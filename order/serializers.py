


from rest_framework import serializers
from .models import Address


from rest_framework import serializers
from django.urls import reverse
from .models import Order,OrderedItem,OrderAddress
from django.contrib.auth import get_user_model
User = get_user_model()



    


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user']



class OrderedItemSerializer(serializers.ModelSerializer): # level 1 small data
    total_price=serializers.SerializerMethodField()
    class Meta:
        model = OrderedItem
        fields = ['id','name','image','price','total_price','quantity','product_id']
    def get_total_price(self,obj):
         return obj.price*obj.quantity
