#CATERING PROGECT

# PEOPLE
1. Sergiy - DEVELOPER (implementor)
2. Carl - client (ADMIN)
3. Martin - Melange
4. Bob - Bueno
5. John - user1 (USER)
6. Marry - user2 (USER)

# PROJECT MANAGMENT

1. Waterfall
2. Scrum - sprint


# MEETINGS

1. Daily Standup Meeting - 15 minutes
2. review meeting - 1 hour
3. grooming meeting - 1 hour(BIG BUSINESSPROBLEM -> small technical features)
4. task meeting - 1 hour(we rent in pool reqwest)


# INPUT DATA

we already have the frontend aplication. Only the backand API isleft...


#  BACKLOG

1. User Managment( CRUD for '/users '). EPIC (from Jira)

    -Entrpoints to implement:

    - USER STORY (from Jira)
    - HTTP POST/users  - create user -> '201 user'(user)
    - HTTP PATCH/users/id - updte users -> '200 users'(admin,user)
    - HTTP DELETE/users - delete users -> '204 users'(user)
    - HTTP GET/users/id - get users -> '200 users'(admin,user)

    -HTTP POST /users/password/forgot -> KEY[UUID]
    -HTTP POST /users/password/change?key=UUID&creds={} -> 200

- Roles:
    -  Admin 
    -  User 
    -  Suport


2. Authentification & Autorization

    - 'HTTP POST / token [USER,ADMIN]'

3. Dishes Managment

    - 'HTTP POST / dishes' - create a new dish (admin)
    - 'HTTP GET/dishes' - all dishes (admin,user,sup)
    - 'HTTP GET/dishes/ID' - retrive dish (admin,user,sup)
    - 'HTTP PUT/dishes/ID' - update dish (admin)
    - 'HTTP DELETE/dishes/ID' - delete dish (admin)

- Refresh the data from restaurants

    - as a 'Thread(deamon=True)'



- Display of recommended dishes for events (_v2_)

4. Order Managment (includes delivery managment in a background)

    - 'HTTP POST / orders' - create new order (user)
        - '{dishes: list[OrderDish]}'
    - 'HTTP GET/orders' - list all orders (admin,sup)
    - 'HTTP GET/orders/ID' - retrive order (admin,user)
    - 'HTTP PUT/orders/ID' - update order (admin)
    - 'HTTP DELETE/orders/ID' - delete order (admin)
    - 'HTTP POST / orders/id/reorder' - reorder faild order (admin,sup)
        - check if status is 'faild'

Order Public Contract
    PYTHON:
enum Provider:
    UKLON
    UBER

class DeliveryInfo:
    provider: Provider
    coordinates: list[float, float]

class Cooking:
    coments: str

enum State:
    WAITING
    COOKING
    DELIVERY
    DELIVERED
    FAILED
    CANCELED_BY_CLIENT
    CACELED_BY_REST
    CANCELED_BY_DELIVERY
    WAITING_ADMIN_APPROVE

class Order
    id: UUID
    state: State
    total: int
    cookinf: CookingInfo | None = None
    delivery: DeliveryInfo | None = None
    

# INVALID APPROACH
# HTTP POST order(dishes) -> DB_SAVE -> ORDER REST(order) -> CALLBACK -> ORDER DELIVERY (REST, CLIENT) -> RESULT

5. Delivery Managment
    - 'HTTP POST /' - create new order (user)
        - '{dishes: list[OrderDish]}'
    - 'HTTP GET/orders' - list all orders (admin,sup)
    - 'HTTP GET/orders/ID' - retrive order (admin,user)
    - 'HTTP PUT/orders/ID' - update order (admin)
    - 'HTTP DELETE/orders/ID' - delete order (admin)
    - 'HTTP POST / orders/id/reorder' - reorder faild order (admin)

6. Payment Processing

7. Communication and Support
    - 'HTTP POST / support/issues/orders/ID' - issue the order question
        - {message: str, photos: list[bytes]}
        - [USER]



# 




