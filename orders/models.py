from django.contrib.auth.models import User
from django.db import models

class Order(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    eternal_order_id = models.CharField(max_length=255)
