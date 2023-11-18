from django.shortcuts import render
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.request import Request

from .models import Myuser, Product,Order
from .serializers import UserSeraializer,LoginSerializer,ProductSerializer,OrderSerializer,CreateOrderSerializer,GetorderSerializer,GetProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import views
from .permissions import IsAdmin,IsAdminOrReadOnly
from rest_framework import renderers





# Create your views here.
class Getroutes(GenericAPIView):
    renderer_classes = [renderers.JSONRenderer]

    def get(self,request,*args,**kwargs):

        routes = {
           'POST': '/adminlogin/',
           'POST': '/create-product/',
           'GET, PUT, DELETE': '/get-product/<str:name>/',
           'GET': '/orders/',
           'POST': '/createorder/<str:name>/',
           'GET, PUT, DELETE' : '/get-order/int:pk/'
        }
        return Response(routes)

class AdminLogin(TokenObtainPairView):
    queryset = Myuser.objects.filter(is_admin = True)
    serializer_class = LoginSerializer
    renderer_classes = [renderers.JSONRenderer]


    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try :
            token = response.data.get('access')
        except:
            token = None
        if token is not None:
            access_token = AccessToken(token)
            user = Myuser.objects.get(id= access_token.payload.get('user_id'))

            if user.is_admin == False :
                return Response({
                    'Not admin': 'User is not admin',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
            else:
                response.data['user_id'] = user.id
                response.data['email'] = user.email
                response.data['username'] = user.username
                response.data['status'] = status.HTTP_200_OK
                return response
            
class CreateProduct(CreateModelMixin,GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [IsAdmin]
   
    def post(self,request, *args,**kwargs):
        return self.create(request,*args,**kwargs)




    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            res = {
                'status': status.HTTP_201_CREATED,
                'product_name': serializer.data.get('name'),
                'product_price': serializer.data.get('product_price'),
                'product_about':serializer.data.get('product_about'),
                
            }
            return Response(res)

class GetProduct(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'name'
    renderer_classes = [renderers.JSONRenderer]
    

    def get(self,request,*args,**kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        serializer.data['status'] = status.HTTP_200_OK 
        
        return Response(serializer.data)
    
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response['status'] = status.HTTP_200_OK
        return response
   
    def delete(self,request,name):
        return self.destroy(request, name )
    
class OrderList(ListAPIView):
    queryset = Order.objects.filter(is_complete = False)
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin]
    renderer_classes = [renderers.JSONRenderer]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
class CreateOrder(CreateModelMixin,GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    lookup_field = 'name'
  
    renderer_classes = [renderers.JSONRenderer]

    def post(self, request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
    def create(self, request, *args, **kwargs):
        product = Product.objects.get(name = kwargs['name'])
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            return self.perform_create(serializer,product)
        else:
            res = {
                'message': 'Invalid-request',
                'status': status.HTTP_400_BAD_REQUEST
            }
         
    def perform_create(self,serializer,product):
        order = serializer.save()
        order.product = product
        order.save()
        
        res = {
            'data':serializer.data,
            
            'status': status.HTTP_201_CREATED
        }

        return Response(res)
    
class Refreshtoken(TokenRefreshView):
    renderer_classes = [renderers.JSONRenderer]

    def post(self, request: Request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class GetOrder(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = GetorderSerializer
    permission_classes = [IsAdmin]
    renderer_classes = [renderers.JSONRenderer]
    lookup_field = 'pk'

    def get(self,request,*args,**kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def update(self, request, *args, **kwargs):
        response =  super().update(request, *args, **kwargs)
        response['status'] = status.HTTP_200_OK
        return response
    
    def delete(self,request,pk):
        return self.destroy(request,pk)
    

        
    
   

   



        


