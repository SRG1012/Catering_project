from rest_framework import status, permissions, viewsets, routers
from rest_framework.response import Response

from .serializers import UserRegistrationSerialazer, UserPublicSerialazer


# /users: GET POST
class UserAPIViewSet(viewsets.GenericViewSet):
    serializer_class = UserRegistrationSerialazer
    permission_classes = [permissions.AllowAny]


    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return [permissions.AllowAny()]
        elif self.action == None:
            return [permissions.AllowAny()]
        else:
            raise NotImplementedError (f"action is not ready")

    def create(self, request):
        serializer = UserRegistrationSerialazer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
  
        return Response(
            UserPublicSerialazer(serializer.validated_data).data,
            status=status.HTTP_201_CREATED,
        )



    def list(self, request):
        return Response(UserPublicSerialazer(request.user).data,
                        status=status.HTTP_200_OK,)
    

router = routers.DefaultRouter()
router.register(r"users", UserAPIViewSet, basename="user")