from django.db import models
from restaurants.models import Restaurant

class Dish(models.Model):
    name: str = models.CharField(max_length=50)

    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)