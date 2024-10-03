#from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate

#from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
#     usrversel

from django.db.models import Q
from .models import Phone
from .serializers import PhoneSerializer ,PhoneSerializer_to_add,PhoneSearchSerializer
from .pagination import PhonePagination
from django.core.cache import cache
from cart.models import CartItem
from wish_list.models import Wish
from order.models import Order
CACHE_TTL = 60 * 60  # Cache timeout of 1 hour






class GetPhoneAPIView(APIView):  # filter
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    def get(self,request,brand,hp,lp):
        print('brand',brand,'hp',hp,'lp',lp)
        all_obj = Phone.objects.filter().order_by('-price')
        if brand!='any':all_obj = all_obj.filter(brand=brand)
        if hp!='any':
             hp=int(hp)
             all_obj = all_obj.filter(price__lte=hp)
        if lp!='any':
            lp=int(lp)
            all_obj = all_obj.filter(price__gte=lp)
         # Pagination
        paginator = PhonePagination()
        result_page = paginator.paginate_queryset(all_obj, request)
        serializer = PhoneSerializer(result_page, many=True,status=status.HTTP_200_OK)

        return paginator.get_paginated_response(serializer.data)

class GetALLPhoneAPIView(APIView):  # filter
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    def get(self, request):
        # Get all phones and order them by price (ascending order)
        all_obj = Phone.objects.all().order_by('-price')
        
        # Initialize the paginator
        paginator = PhonePagination()
        
        # Paginate the query set
        result_page = paginator.paginate_queryset(all_obj, request)
        
        # Serialize the paginated data
        serializer = PhoneSerializer(result_page, many=True)
        
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)




# class GetPhoneWithIdAPIView(APIView):  # phone by id
#     authentication_classes = [JWTAuthentication, SessionAuthentication]
#     def get(self,request,id):
#         try:
#             user_id=0
#             if request.user:user_id=request.user.id
#             all_obj = Phone.objects.get(id=id)
#             serializer = PhoneSerializer(all_obj,many=False,context={'user_id': user_id})
           
#             return Response({'phone':serializer.data})
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        






class GetPopular_phone(APIView):  # popular
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    def get(self,request):
        try:
            user_id=0
            if request.user:user_id=request.user.id
            all_obj = Phone.objects.filter().order_by('-total_sold')[:8]
            serializer = PhoneSerializer(all_obj,many=True,context={'user_id': user_id})
            return Response({'all_phones':serializer.data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class latest_phone(APIView): 
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    def get(self,request):
        try:
            all_obj = Phone.objects.filter().order_by('-date_created')[:8]
            serializer = PhoneSerializer(all_obj,many=True)
            return Response({'all_phones':serializer.data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class PhoneSearchView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    serializer_class = PhoneSearchSerializer
    def post(self, request):
         try:
            user=request.user
            user_id=0
            if request.user:user_id=request.user.id
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            search_query = serializer.validated_data.get('search_query')

            # Generate cache key based on the search query
            cache_key = f"phone_search_{search_query.lower()}"
            
            # Check if the result is in the cache
            cached_result = cache.get(cache_key)
            print("hello aslma")
            if cached_result:
                print('helo')
                for single_phone in cached_result:
                    product=Phone.objects.get(id=single_phone['id'])
                    single_phone['purchased_by_current_user'] =False
                    single_phone['is_in_cart']=False
                    single_phone['is_in_wishlist']=False
                    if request.user.is_authenticated:
                        # set is_in_cart
                        single_phone['is_in_cart']= CartItem.objects.filter(cart=user.my_cart,product=product).exists()
                        # set is_in_wishlist
                        single_phone['is_in_wishlist']= Wish.objects.filter(user=user,phone=product).exists()
                        # set purchased_by_current_user
                        flag=False
                        all_succesful_order= Order.objects.filter(status='complete',user=user)
                        for single_order in all_succesful_order:
                            if flag:break
                            all_itmes = single_order.items.all()
                            for single_item in all_itmes:
                                if single_item.product_id==product.id:
                                     single_phone['purchased_by_current_user']=True
                                     flag=True
                                     break
              
                return Response({'all_phones': cached_result},status=status.HTTP_200_OK)

            # Search in the database if not in the cache
            phones = Phone.objects.filter(
                Q(brand__icontains=search_query) |
                Q(model__icontains=search_query) |
                Q(price__icontains=search_query) |
                Q(ram__icontains=search_query) |
                Q(slug__icontains=search_query)
            )
            print('from data base')
            # Serialize the results
            phone_serializer = PhoneSerializer(phones, many=True,context={'user_id': user_id})
            cache.set(cache_key, phone_serializer.data, CACHE_TTL)
            return Response({'all_phones': phone_serializer.data})


            # # Try setting a value in the cache
            # cache.set('monir', 'akalu_aslma', CACHE_TTL)

            # # Try retrieving the value from the cache
            # value = cache.get('monir')
            # print(value)  
            # return Response({'all_phones': 200})
        
         except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)