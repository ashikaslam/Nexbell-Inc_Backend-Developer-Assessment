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


#from . import Utility_function
#from extra_fruction import problem_solver

from. import serializers
from mobilephone. models import Phone
from.models import Cart,CartItem
from django.contrib.auth import get_user_model
User = get_user_model()
from wish_list .models import Wish



class add_to_cart(APIView): 
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,id): # this is a id of a phone obj
        try:
            user = request.user
            phone =  Phone.objects.get(id=id)
            if Wish.objects.filter(user=user,phone=phone).exists():
                Wish.objects.filter(user=user,phone=phone).delete()
            my_cart = user.my_cart
            cart_item = CartItem.objects.create(product=phone,cart=my_cart)
            cart_item .cart=my_cart
            return Response({ "status": 1},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class increase_quantity(APIView): 
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id): # this id is a id of cart item
        try:
            cart_item =  CartItem.objects.get(id=id)
            if (not cart_item.cart.user==request.user): return Response(status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity+=1
            cart_item.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class decrease_quantity(APIView): 
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        try:
            cart_item =  CartItem.objects.get(id=id)
            if (not cart_item.cart.user==request.user): return Response(status=status.HTTP_400_BAD_REQUEST)
            if cart_item.quantity>1:cart_item.quantity-=1
            cart_item.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class remove_cart_item(APIView): 
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        try:
            cart_item =  CartItem.objects.get(id=id)
            if (not cart_item.cart.user==request.user): return Response(status=status.HTTP_400_BAD_REQUEST)
            cart_item.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class get_my_cart(APIView): 
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            my_cart = user.my_cart
            all_items = my_cart.items.all()
            serializer = serializers.Cart_items_Serializer(all_items, many=True)
            return Response({'all_items': serializer.data,"in_total":my_cart.in_total()},status=status.HTTP_200_OK)
           
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  
