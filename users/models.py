from django.db import models


class User(models.Model):
    email = models.CharField(max_length=110)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    addres = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
