from datetime import date
from threading import Thread
from time import sleep
from django.db.models import QuerySet

from food.models import Order
from food.enums import OrderStatus




class Processor:

    EXCLUDE_STATUSES = (
        OrderStatus.DELIVERED,
        OrderStatus.NOT_DELIVERED,
    )

    def __init__(self) -> None:
        self._thread = Thread(target=self.process, daemon=True)
        print(f"Orders Processor is created")

    @property
    def today(self):
        return date.today()

    def start(self):
        self._thread.start()
        print(f"Orders Processor started processing orders")


    def process(self):
        """The processing of the orders entrypoint."""

        while True:
            self._process()
            sleep(3)

    def _process(self):
        
        orders: QuerySet[Order] = Order.objects.exclude(
            status__in=self.EXCLUDE_STATUSES,
        )

        for order in orders:
            match order.status:
                case OrderStatus.NOT_STARTED:
                    self._process_not_started(order)
                case OrderStatus.COOKING_REJECTED:
                    self._process_cooking_rejected()

                case _:
                    print(f"Unrecognized order status: {order.status}. passing")


    def _process_not_started(self, order: Order):
        if order.eta > self.today:
            pass
        elif order.eta < self.today:
            order.status = OrderStatus.CENCELLED  
            order.save()
            print(f"Canceled order {order}")  
        else:
            order.status = OrderStatus.COOKING
            order.save()

            restaurants =  set()
            for item in order.items.all():
                restaurants. add(item.dish.restaurant)
            print(f"Finished preparing order. Restaurants: {restaurants}")
            print(f"Order: {order}")


    def _process_cooking_rejected(self):
        raise NotImplementedError