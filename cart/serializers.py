



from rest_framework import serializers
from django.urls import reverse
from .models import Cart,CartItem
from django.contrib.auth import get_user_model
User = get_user_model()


class Cart_items_Serializer(serializers.ModelSerializer): # level 1 small data
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    single_price=serializers.SerializerMethodField()
    total_price=serializers.SerializerMethodField()
    increase_quantity_url = serializers.SerializerMethodField()
    decrease_quantity_url = serializers.SerializerMethodField()
    remove_cart_item_url = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
   

    class Meta:
        model = CartItem
        fields = ['id','name','image','single_price','total_price','quantity','increase_quantity_url',
                 'decrease_quantity_url' ,'remove_cart_item_url','product_id']
        extra_kwargs = {
        #'front_img': {'write_only': True, 'required': False},
        # 'back_img': {'write_only': True, 'required': False},
        'name': {'read_only': True}, 
        'image': {'read_only': True}, 
        'single_price': {'read_only': True}, 
        'total_price': {'read_only': True}, 
        'quantity': {'read_only': True}, 
        'id': {'read_only': True}, 
        'product_id': {'read_only': True}, 
}
   
    def get_name(self, obj):
        return obj.product.name
    def get_product_id (self, obj):
        return obj.product.id
    def get_image(self, obj):
         return obj.product.front_pic
    def get_single_price(self, obj):
         return obj.product.final_price()
    def get_total_price(self, obj):
         return obj.product.final_price()*obj.quantity
    def get_increase_quantity_url(self, obj):
        return reverse('increase-quantity', kwargs={'id': obj.id})
    def get_decrease_quantity_url(self, obj):
        return reverse('decrease-quantity', kwargs={'id': obj.id})
    def get_remove_cart_item_url(self, obj):
        return reverse('remove_cart_item', kwargs={'id': obj.id})