from celery.result import AsyncResult
from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status, viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response

from .services import schedule_order

from .models import Dish, DishOrderItem, Order, Restaurant
from .serializers import DishSerializer, OrderCreateSerializer, RestaurantSerializer
from .enums import OrderStatus


class FoodAPIViewSet(viewsets.GenericViewSet):
    """API для управления блюдами, заказами и ресторанами"""

    #  HTTP GET /food/dishes
    @action(methods=["get"], detail=False)
    def dishes(self, request):
        """ Получить список всех блюд """
        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)
        return Response(serializer.data)

    #  HTTP POST /food/orders
    @action(methods=["post", "get"], detail=False)
    def orders(self, request: WSGIRequest):
        """ Создать новый заказ """

        # 1. Валидируем входные данные
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Проверяем, что данные - это словарь
        if not isinstance(serializer.validated_data, dict):
            raise ValueError("Invalid order format")

        # 3. Опрацювати список страв і визначити ресторани
        restaurant_names = set()
        for dish_order in serializer.validated_data["food"]:
            restaurant_names.add(dish_order["dish"].restaurant.name.lower())

        # 4. Створюємо замовлення з відповідними статусами
        order_kwargs = {
        "user": request.user,
        "eta": serializer.validated_data["eta"],
        }

        if "melange" in restaurant_names:
            order_kwargs["melange_status"] = "not_started"

        if "bueno" in restaurant_names:
            order_kwargs["bueno_status"] = "not_started"

        order = Order.objects.create(**order_kwargs)


        # 5. Создаём позиции заказа
        for dish_order in serializer.validated_data["food"]:
            instance = DishOrderItem.objects.create(
                dish=dish_order["dish"], 
                quantity=dish_order["quantity"], 
                order=order
            )

        schedule_order(order=order)
        print(f"New order created: {order.pk}.\nETA: {order.eta}")
        print(f"New order position: {instance.pk}")

        return Response(data={
        "id": order.pk,
        "melange_status": order.melange_status,
        "bueno_status": order.bueno_status,
        "eta": order.eta,
        "total": 9999,
        }, status=status.HTTP_201_CREATED)


    #  HTTP GET /food/restaurants
    @action(methods=["get"], detail=False)
    def restaurants(self, request):
        """ Получить список всех ресторанов """
        queryset = Restaurant.objects.all()
        serializer = RestaurantSerializer(queryset, many=True)
        return Response(serializer.data)

    #  HTTP POST /food/restaurants
    @action(methods=["post"], detail=False)
    def create_restaurant(self, request):
        """ Создать новый ресторан """
        serializer = RestaurantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    #  HTTP GET /food/restaurants/{id}
    @action(methods=["get"], detail=True)
    def get_restaurant(self, request, pk=None):
        """ Получить ресторан по ID """
        try:
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)


# Роутер для API еды и ресторанов
router = routers.DefaultRouter()
router.register("food", FoodAPIViewSet, basename="food")

