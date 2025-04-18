from time import sleep
from collections import defaultdict
from datetime import datetime, date, time
import uuid


import httpx
import requests
from shared.cache import CacheService
from .enums import Restaurant
from .models import DishOrderItem, Order
from config import celery_app


class OrderInCache:
    def __init__(self) -> None:
        self.orders: dict[str, dict [str, str | list[dict]]] = defaultdict(dict)


    def append(self, restaurant: str, item: DishOrderItem):
        if not self.orders[restaurant]:
            self.orders[restaurant] ={
                "external_id": "",
                "status": "not_started",
                "dishes": [
                    {
                    "dish": item.dish.name,
                    "quantity": item.quantity,
                    }
                ]
            }
        else:
            self.orders[restaurant]["dishes"].append(
                {
                    "dish": item.dish.name,
                    "quantity": item.quantity,
                }
            )

#@celery_app.task
def melange_order_processing(order: Order):
    """Обробляє замовлення для ресторану MELANGE поетапно."""
    print(f"[MELANGE] Start processing order #{order.pk}")

    while order.melange_status != "finished":
        print(f"[MELANGE] Current status: {order.melange_status}")

        if order.melange_status == "not_started":
            if not order.melange_external_id:
                payload = {
                    "order": [
                        {
                            "dish": item.dish.name,
                            "quantity": item.quantity,
                        }
                        for item in order.items.all()
                        if item.dish.restaurant.name.lower() == "melange"
                    ]
                }
                response = httpx.post("http://localhost:8001/api/orders", json=payload)
                response.raise_for_status()

                external_id = response.json()["id"]
                order.melange_external_id = external_id
                order.save(update_fields=["melange_external_id"])
                print(f"[MELANGE] External order created. ID = {external_id}")
            else:
                response = httpx.get(f"http://localhost:8001/api/orders/{order.melange_external_id}")
                response.raise_for_status()

                new_status = response.json()["status"]
                order.melange_status = new_status
                order.save(update_fields=["melange_status"])
                print(f"[MELANGE] Status updated to: {new_status}")
                sleep(1)

        elif order.melange_status == "cooking":
            response = httpx.get(f"http://localhost:8001/api/orders/{order.melange_external_id}")
            response.raise_for_status()

            new_status = response.json()["status"]
            order.melange_status = new_status
            order.save(update_fields=["melange_status"])
            print(f"[MELANGE] Cooking in progress. New status: {new_status}")
            sleep(3)

        elif order.melange_status == "cooked":
            print(f"[MELANGE] Order cooked. Ready to call delivery (not implemented).")
            raise NotImplementedError("Delivery integration is not implemented yet")

        else:
            raise ValueError(f"[MELANGE] Unknown status: {order.melange_status}")


def bueno_order_processing(order: OrderInCache):
    print("BUENO===========================")
    print(order.orders)
    print("BUENO===========================")



 
 
@celery_app.task
def _schedule_order(order: Order):
    melange_items = []
    bueno_items = []

    for item in order.items.all():
        restaurant = item.dish.restaurant.name.lower()
        if restaurant == Restaurant.MELANGE:
            melange_items.append(item)
        elif restaurant == Restaurant.BUENO:
            bueno_items.append(item)
        else:
            raise ValueError(f"Can not create order for {item.dish.restaurant.name}")

    if melange_items:
        melange_order_processing(order)
    if bueno_items:
        bueno_order_processing(order)


    # order_key = str(uuid.uuid4())
    # cache = CacheService()

    # cache.set(namespace="restaurant_order", key=order_key, instance=order_in_cache.orders)
    
    # melange_order_processing(order_in_cache)
    # bueno_order_processing(order_in_cache)
 

def schedule_order(order: Order):
    assert isinstance(order.eta, date)

    if order.eta == date.today():
        print("The order will be started processing now")
        return _schedule_order.delay(order)
    else:
        eta = datetime.combine(order.eta, time(hour=3))
        print(f"The order will be started processing {eta}")
        return _schedule_order.apply_async(args=(order,), eta=eta)
