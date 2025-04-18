from django.db import models
from django.conf import settings


class Restaurant(models.Model):
    class Meta:
        db_table = "restaurants"

    name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"[{self.pk}] {self.name}"


class Dish(models.Model):
    class Meta:
        db_table = "dishes"
        verbose_name_plural = "dishes"

    name = models.CharField(max_length=50, null=True)
    price = models.IntegerField()
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} {self.price}  ({self.restaurant})"


class Order(models.Model):
    """
    The instance of that class defines the order of dishes from
    external restaurants that are available in the system.
    """

    class Meta:
        db_table = "orders"


    melange_external_id = models.CharField(max_length=255, null=True, blank=True)
    melange_status = models.CharField(max_length=30, default="not_started")

    bueno_external_id = models.CharField(max_length=255, null=True, blank=True)
    bueno_status = models.CharField(max_length=30, default="not_started")

    eta = models.DateField()
    provider = models.CharField(max_length=20, null=True, blank=True)  # still usable for quick filtering
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Order #{self.pk} for {self.user.email}"

    def __repr__(self) -> str:
        return f"<Order #{self.pk} for {self.user.email}>"


class DishOrderItem(models.Model):
    """the instance of that class defines a DISH item that is related
    to an ORDER, that user has made.
    """

    class Meta:
        db_table = "dish_order_items"

    quantity = models.SmallIntegerField()

    dish = models.ForeignKey("Dish", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")
    


    def __str__(self) -> str:
        return f"[{self.order.pk}] {self.dish.name}: {self.quantity}"
    

