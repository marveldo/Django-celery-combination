from rest_framework import serializers
from rest_framework.fields import empty
from .models import Myuser,Product,Order
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserSeraializer(serializers.ModelSerializer):
   
    class Meta:
        model = Myuser
        fields = ['username','email','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Myuser(
            username=validated_data['username'],
            email=validated_data['email'],
            
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user

class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    default_error_messages = {
        'no_active_account': 'Your account is not active',
        'Invalid_Credentials': 'Your Login failed',
        'no_admin_account': 'account doesnt have admin access'
    }
class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
    def __init__(self,*args,**kwargs):
        super(GetProductSerializer,self).__init__(*args,**kwargs)
        for fieldname,field in self.fields.items():
            field.required = False

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['is_featured']

    def __init__(self, *args, **kwargs):
        super(ProductSerializer,self).__init__(*args, **kwargs)

        for fieldname,field in self.fields.items():
            field.required = True

class UpdateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    
    product = ProductSerializer()

    class Meta:
        model = Order
        fields = '__all__'

class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = ['product','is_complete']  

    def __init__(self, *args, **kwargs):
        super(CreateOrderSerializer,self).__init__(*args, **kwargs)

        for fieldname,field in self.fields.items():
            field.required = True  

class GetorderSerializer(serializers.ModelSerializer):

    product = UpdateProductSerializer()

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GetorderSerializer,self).__init__(*args, **kwargs)

        for fieldname,field in self.fields.items():
            field.required = False 

