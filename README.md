# ТЕХНОЛОГІЧНИЙ СТЕК


Python - мова програмування
Django - веб-фреймворк
DRF (Django REST Framework) - перевірка даних
PostgreSQL - База даних (RDBMS)
Таблиці
Redis/MongoDB - Сховище ключ-значення
json {"будь-який ключ": значення}
Керування залежностями...


УСТАНОВКИ
# activate virtual environment
pipenv shell --python python3.12


# generate `Pipfile.lock` file after adding dependencies
pipenv lock

# install dependencies form `Pipfile.lock` file
pipenv sync




# TABLES

'''python
class User:
    id: int
    
    

'''



# JSON
python manage.py loaddata food/fixtures/test_data.json


# ABOUT Django & DRF
# Django concepts
View - endpoint ('HTTP POST /users', create user, 'UserView', SSR (using Django Templates), MVT, Return HTML document)
Forms - HTML ('<input>', SSR (using Django Templates), MVT)
Models - ORM ('Data Access Layer', database tables, migrations, admin)
Admin - battery (SSR (using Django Templates))

# DRF concepts
APIViews (inherited from Views, implement JsonResponse, Content-Type: application-json)
Serializers (data validations, aka @dataclass)

"""python
class User(models.Model):
    email = models.EmailField(...)
    password = models.CharField(...)

# http request body
class UserInputStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# public stucture
class UserOutputStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserAPIView(generics.EverythingAPIView):
    model = User
    serializer_class = UserSerializser
    pk = "id"


urlpatterns = [
    path("users/", UserAPIView.as_view())
]

# HTTP POST /users
#   RequestBody: __all__
# HTTP GET /users
#   list[User]
# HTTP GET /users/7
#   User
# HTTP PUT /users/7
#   RequestBody: first_name, last_name
#   User
# HTTP DELETE /users/7
#   204
"""


#  HASH FUNCTIONS

#  ATTRIBUTES

1. fixed size (string)
2. fast
3. avalanche (лавиноподібність)
     3.1 john -> 527bd5b5d689e2c32ae974c6229ff785 
     3.1 john1 -> e06ce282ec5c0f9701ec03d10690b2af 
     3.1 johna -> aa8e7e8c8894f55dceb668662106bc7a
4. collision-free
5. determined (john hash always the same)


#  LIST

1. MD5
2. SHA1
3. SHA2
4. SHA3


# ViewSets

'''python
class UserViewSet(viewsets.ViewSet):
    def list(self, request):  # HTTP GET /users
        pass

    def create(self, request): # HTTP POST /users
        pass

    def retrieve(self, request, pk=None): # HTTP GET /users/pk
        pass

    def update(self, request, pk=None): # HTTP PUT /users/pk
        pass

    def partial_update(self, request, pk=None):  # HTTP PATCH /users/pk
        pass

    def destroy(self, request, pk=None): # HTTP DELETE /users/pk
        pass
'''

# Old code

# def create_user(request):
#     if request.method == "POST":
#         raise NotImplementedError
    
#     data = json.loads(request.body)
#     user = User.objects.create_user(**data)

#     return = {
#         "id": user.id,
#         "email": user.email,
#     }

#     return JsonResponse(results)  

# class UserSerializser(serializers.ModelSerializer):
#     class Meta:
#         model = User 
#         fields = "__all__" -->



# PROJECT INFRASTRUCTURE
1. application (Python, Django (FastAPI))
2. database (SQLite3, PosgreSQL)
3. cache (Redis, Memcached, Valkey)
4. worker (Python, RQ, Celery)
5. queue (broker, RabbitMQ, SQS, Redis)