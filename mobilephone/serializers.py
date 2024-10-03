from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from .models import Phone
from wish_list.models import Wish
from cart . models import Cart,CartItem


from rest_framework import serializers
from .models import Phone
from order.models import Order,OrderedItem




class PhoneSerializer_to_add(serializers.ModelSerializer):
    front_img = serializers.ImageField(required=False)
    back_img = serializers.ImageField(required=False)
    class Meta:
        model = Phone
        exclude = ['slug','front_pic', 'back_pic','total_sold']  # Exclude the slug field from being serialized

        

    
    




class PhoneSerializer(serializers.ModelSerializer):



    # Add write-only fields for images
    front_pic = serializers.ImageField(write_only=True, required=False)
    back_pic = serializers.ImageField(write_only=True, required=False)
    
    is_in_wishlist = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()
    purchased_by_current_user = serializers.SerializerMethodField()

    avg_rating = serializers.SerializerMethodField()
    class Meta:
        model = Phone
        fields = "__all__"
        extra_kwargs = {
             'front_pic': {'write_only': True},  
             'back_pic': {'write_only': True},  
            
              'front_pic': {'read_only': True}, 
              'back_pic': {'read_only': True}, 
              'is_in_wishlist': {'read_only': True},
              'is_in_cart': {'read_only': True},
              'avg_rating': {'read_only': True},
              'purchased_by_current_user': {'read_only': True},
              'total_sold': {'read_only': True},
                }
    def get_is_in_wishlist(self, obj):
        try:
            user_id = self.context.get('user_id')
            if not User.objects.filter(id=user_id).exists():return False
            user = User.objects.get(id=user_id)
            return Wish.objects.filter(user=user,phone=obj).exists()
        except Exception as e:return False

    def get_is_in_cart(self, obj):
        try:
            user_id = self.context.get('user_id')
            if not User.objects.filter(id=user_id).exists():return False
            user = User.objects.get(id=user_id)
            return CartItem.objects.filter(cart=user.my_cart,product=obj).exists()
        except Exception as e:return 
        
    def get_purchased_by_current_user(self, obj):
        try:
            user_id = self.context.get('user_id')
            if not User.objects.filter(id=user_id).exists():return False  
            user= User.objects.get(id=user_id)
            all_succesful_order= Order.objects.filter(status='complete',user=user)
            for single_order in all_succesful_order:
                all_itmes = single_order.items.all()
                for single_item in all_itmes:
                    if single_item.product_id==obj.id:return True
        except Exception as e:return False
    

    def get_avg_rating(self, obj):
        try:
            return obj.avg_rating()
        except Exception as e:return 0    
   
            
   


class PhoneSearchSerializer(serializers.Serializer):
    search_query = serializers.CharField(max_length=255, required=True)
