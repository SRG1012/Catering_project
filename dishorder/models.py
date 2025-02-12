from django.db import models
from dishes.models import Dish
from orders.models import Order

class DishOrder(models.Model):
    quantity = models.SmallIntegerField()

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
