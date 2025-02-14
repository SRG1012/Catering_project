from django.db import models

PROVIDERS_CHOICES = (
    ('uklon', 'Uklon'),
    ('uber', 'Uber'),
)

DELIVERY_STATUSES_CHOICES = (
    ("NOT STARTED", "Not started"),
    ("ONGOING", "Ongoing (in delivery)"),
    ("cancelled user", "Canceled by User (customer)"),
    ("cancelled system", "Canceled by System"),
    ("cancelled driver", "Canceled by Driver"),
    ("delivered", "Delivered"),
    ("stolen", "Stolen by Driver"),
)


class DeliveryDishesOrder(models.Model):

    class Meta:
        db_table = "dishes_orders_deliveries"

    provider = models.CharField(max_length=100, choices=PROVIDERS_CHOICES)
    status = models.CharField(max_length=50, choices=DELIVERY_STATUSES_CHOICES)
    adresses = models.TextField()
    external_order_id = models.CharField(max_length=255)

    order = models.ForeignKey('food.DishesOrder', on_delete=models.CASCADE)
