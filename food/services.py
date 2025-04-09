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
def melange_order_processing(order: OrderInCache):
    while (current_status := order.orders[Restaurant.MELANGE]["status"]) != "finished":
        if current_status == "not_started":
            if not order.orders[Restaurant.MELANGE]["external_id"]:
                payload = {"order": order.orders[Restaurant.MELANGE]["dishes"]}
                response = httpx.post(
                    "http://localhost:8001/api/orders", 
                    json=payload)
                response.raise_for_status()
                order.orders[Restaurant.MELANGE]["external_id"] = response.json()["id"]
            else:
                external_order_id = order.orders[Restaurant.MELANGE]["external_id"]
                response = httpx.get(
                    f"http://localhost:8001/api/orders/{external_order_id}")
                response.raise_for_status()
                order.orders[Restaurant.MELANGE]["status"] = response.json()["status"]
                print(f"Current status is {current_status}. Waiting 1 second")
                sleep(1)
        elif current_status == "cooking":
            external_order_id = order.orders[Restaurant.MELANGE]["external_id"]
            response = httpx.get(
                f"http://localhost:8001/api/orders/{external_order_id}") 
            response.raise_for_status()
            order.orders[Restaurant.MELANGE]["status"] = response.json()["status"]
            sleep(3)
            print(f"Current status is {current_status}. Waiting 3 second")
        elif current_status == "cooked":
            #print(f"CALLING DELIVERY SERVICE TO PASS THE FOOD DRIVER")
            raise NotImplementedError("delivery is not implemented yet")
        else:
            raise ValueError(f"Status {current_status} is not supported")

def bueno_order_processing(order: OrderInCache):
    print("BUENO===========================")
    print(order.orders)
    print("BUENO===========================")



 
 
@celery_app.task
def _schedule_order(order: Order):

    # melange_order: list[DishOrderItem] = []
    # bueno_order: list[DishOrderItem] = []

    order_in_cache = OrderInCache()

    for item in order.items.all():
        if (restaurant := item.dish.restaurant.name.lower()) == Restaurant.MELANGE:
            order_in_cache.append(restaurant, item)
        elif item.dish.restaurant.name.lower() == Restaurant.BUENO:
            order_in_cache.append(restaurant, item)
        else:
            raise ValueError(f"Can not create order for {item.dish.restaurant.name} restaurant")


    order_key = str(uuid.uuid4())
    cache = CacheService()

    cache.set(namespace="restaurant_order", key=order_key, instance=order_in_cache.orders)
    
    melange_order_processing(order_in_cache)
    bueno_order_processing(order_in_cache)
 

def schedule_order(order: Order):
    """Add the task to the queue for the future processing."""
 
    assert type(order.eta) is date

    # _schedule_order(order)
    # return None
 
    if order.eta == date.today():
        print(f"The order will be started processing now")
        return schedule_order.delay(order)
    else:
        eta = datetime.combine(order.eta, time(hour=3))
        print(f"The order will be started processing {eta}")
        return schedule_order.apply_async(args=(order,), eta=eta)