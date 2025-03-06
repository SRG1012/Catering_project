from django.contrib import admin
from django.http.response import HttpResponseRedirect
from .models import Dish, Restaurant, Order, DishOrderItem


admin.site.register(Restaurant)





def import_csv(self, request, queryset):
    print("import_csv")
    return HttpResponseRedirect("/import-dishes")

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "restaurant")
    search_fields = ("name",)  
    list_filter = ("name", "restaurant")
    actions = ("import_csv",)

    
#admin.site.register(DishOrderItem)
class DishOrderItemInline(admin.TabularInline):
    model = DishOrderItem


@admin.register(Order)
class DishesOrderAdmin(admin.ModelAdmin):
    inlines = (DishOrderItemInline,)


admin.site.add_action(import_csv)



