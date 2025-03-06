from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status, viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Dish, DishOrderItem, Order, Restaurant
from .serializers import DishSerializer, OrderCreateSerializer, RestaurantSerializer
from .enums import OrderStatus


class FoodAPIViewSet(viewsets.GenericViewSet):
    """API для управления блюдами и заказами"""

    #  HTTP GET /food/dishes
    @action(methods=["get"], detail=False)
    def dishes(self, request):
        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)
        return Response(serializer.data)

    #  HTTP POST /food/orders
    @action(methods=["post"], detail=False)
    def orders(self, request: WSGIRequest):

        # 1. Валидируем входные данные
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #  2. Проверяем, что данные - это словарь
        if not isinstance(serializer.validated_data, dict):
            raise ValueError("Invalid order format")

        # 3. Создаём новый заказ
        order = Order.objects.create(
            status=OrderStatus.NOT_STARTED,
            user=request.user,
        )
        print(f" New order created: {order.pk}")

        #  4. Получаем список блюд
        try:
            dishes_order = serializer.validated_data["food"]
        except KeyError:
            raise ValueError(" Error: The order is incorrectly composed")

        #  5. Создаём позиции заказа
        for dish_order in dishes_order:
            instance = DishOrderItem.objects.create(
                dish=dish_order["dish"], 
                quantity=dish_order["quantity"], 
                order=order
            )
            print(f"New order position: {instance.pk}")

        return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)


#  Роутер для API еды
router = routers.DefaultRouter()
router.register("food", FoodAPIViewSet, basename="food")


class RestaurantViewSet(viewsets.ViewSet):
    
    # HTTP GET /restaurants
    def list(self, request):
        """ Получить список всех ресторанов """
        queryset = Restaurant.objects.all()
        serializer = RestaurantSerializer(queryset, many=True)
        return Response(serializer.data)

    #  HTTP POST /restaurants
    def create(self, request):
        """ Создать новый ресторан """
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #  HTTP GET /restaurants/{id}
    @action(detail=True, methods=["get"])
    def retrieve(self, request, pk=None):
        """ Получить ресторан по ID """
        try:
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)


restaurant_router = routers.DefaultRouter()
restaurant_router.register("restaurants", RestaurantViewSet, basename="restaurants")
