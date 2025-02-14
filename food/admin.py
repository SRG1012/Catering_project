from django.contrib import admin
from .models import Dish, Restaurant, DishesOrder, DishOrderItem

#admin.site.register(Dish)
#admin.site.register(Restaurant)
#admin.site.register(DishesOrder)
#admin.site.register(DishOrderItem)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address")
    search_fields = ("name", "address")

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "restaurant")
    search_fields = ("name",)
    list_filter = ("restaurant",)


#admin.site.register(DishOrderItem)
class DishOrderItemInline(admin.TabularInline):
    #model = DishOrderItem
    list_display = ("id", "order", "dish", "quantity")

@admin.register(DishesOrder)
class DishesOrderAdmin(admin.ModelAdmin):
    #inlines = (DishOrderItemInline,)
    list_display = ("id", "external_order_id", "user")


