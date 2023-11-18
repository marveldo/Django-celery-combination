from .views import AdminLogin,CreateProduct,GetProduct,OrderList,CreateOrder,Getroutes,Refreshtoken,GetOrder
from django.urls import path

urlpatterns = [
    path('',Getroutes.as_view()),
    path('adminlogin/',AdminLogin.as_view()),
    path('create-product/',CreateProduct.as_view()),
    path('get-product/<str:name>/', GetProduct.as_view()),
    path('orders/',OrderList.as_view()),
    path('createorder/<str:name>/',CreateOrder.as_view()),
    path('refreshtoken/',Refreshtoken.as_view()),
    path('get-order/<int:pk>/',GetOrder.as_view())
 
] 