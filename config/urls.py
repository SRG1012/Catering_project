from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.api import router as users_router
from food.api import router as food_router

urlpatterns = (
    [
    # USERS MANAGMENT
    #=====================
    path('admin/', admin.site.urls),
    path('auth/token/', TokenObtainPairView.as_view()),
    #=====================
    # path('import-dishes/', import_dishes),
    # path("users/", user_create_retrieve),
    # path("users/<id:int>", user_update_delete),
    # path("users/password/forgot", password_forgot),
    # path("users/password/change", password_change),
    #auth 
    #=====================
    #  path("auth/token", access_token), 
    #BASKET & ORDER MANAGMENT
    #=====================
    # path("basket/", basket_create),
    # path("basket/<id:int>/dishes", basket_retrieve),
    # path("basket/<id:int>/dishes/<id:int>", basket_dish_add_update_delete), 
    # path("basket/<id:int>/order", order_from_basket),
    # path("orders/<id:int>/", order_details), 
    ] 
    + users_router.urls 
    + food_router.urls
)