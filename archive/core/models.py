from django.db import models

class User(models.Model):
    email = models.CharField(max_length=110)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    addres = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100) 


class Order(models.Model):
    eternal_order_id = models.CharField(max_length=255)
    
    user: User = models.ForeignKey('User', on_delete=models.CASCADE)
    

class Dish(models.Model):
    name: str = models.CharField(max_length=50)

    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE
    )

class DishOrder(models.Model):
    quantity = models.SmallIntegerField()

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)

class DeliveryOrder(models.Model):
    provider = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    adresses = models.TextField()
    external_order_id = models.CharField(max_length=255)

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
