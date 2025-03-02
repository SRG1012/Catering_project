import operator
from django.contrib import admin
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest 
from django.urls import path
from food.views import import_dishes

from dataclasses import dataclass, asdict

@dataclass
class Dish:
    id: int
    name: int
    price: int
    restaurant: int

@dataclass
class Basket:
    id: int
    


@dataclass    
class BasketItem:
    id: int


storage = {
    "dishes": [
        Dish(id =1, name="salad", price = 100, restaurant=1),
        Dish(id =2, name="pizza", price = 150, restaurant=2),
        Dish(id =3, name="sushi", price = 200, restaurant=1),   
        ],
    "baskets": [
        # BasketCreateRequestBody(id=1),
    ],
    "basket_items": [
    #     BasketItem(id=1,basket_id=1, dish_id=1, quantity=2),
    #     BasketItem(id=2,basked_id=1, dish_id=3, quantity=1),
    ]
}





def basket_create(request: WSGIRequest):
    if request.method != "POST":
        raise ValueError(f"Method {request.method} not allowed")
    else:
        try:
            last_basket: Basket = sorted(storage["baskets"], key=operator.attrgetter("id"))[-1]
        except IndexError:
            last_id = 0
        else:
            last_id = last_basket.id

        instance = Basket(id=last_basket + 1)
        storage["baskets"].append(instance)
        print(storage["baskets"])
        return JsonResponse(asdict(instance))

urlpatterns = [
    # USERS MANAGMENT
    #=====================
    path('admin/', admin.site.urls),
    path('import-dishes/', import_dishes),

    # path("users/", user_create_retrieve),
    # path("users/<id:int>", user_update_delete),
    # path("users/password/forgot", password_forgot),
    # path("users/password/change", password_change),
    #auth 
    #=====================
    #  path("auth/token", access_token), 
    #BASKET & ORDER MANAGMENT
    #=====================
    path("basket/", basket_create),
    # path("basket/<id:int>/dishes", basket_retrieve),
    # path("basket/<id:int>/dishes/<id:int>", basket_dish_add_update_delete), 
    # path("basket/<id:int>/order", order_from_basket),

    # path("orders/<id:int>/", order_details), 
]