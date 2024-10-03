
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
from django.shortcuts import get_object_or_404






from .models import  Rating
from mobilephone.models import Phone 
from .serializers import RatingSerializer
from rest_framework.permissions import IsAuthenticated
from order.models import Order,OrderedItem


class AddRatingView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer
    def post(self, request,product_id):
        try:
            
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = request.user

            did_he_buy_this_product=False
            all_succesful_order= Order.objects.filter(status='complete',user=user)
            for single_order in all_succesful_order:
                if did_he_buy_this_product:break
                all_itmes = single_order.items.all()
                for single_item in all_itmes:
                    if single_item.product_id == product_id:
                      did_he_buy_this_product=True
                      break


            print("did_he_buy_this_product> ",did_he_buy_this_product,' user> ',user)
            if not  did_he_buy_this_product: return Response(status=status.HTTP_401_UNAUTHORIZED)
            rating = serializer.save(user=user, phone=phone)
            return Response({"status": "success", "rating_id": rating.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class Get_comments_for_a_PhoneWithIdAPIView(APIView):  # comments  by phone  id
    def get(self,request,product_id):
        try:
            phone = get_object_or_404(Phone,id= product_id)
            all_comments = Rating.objects.filter(phone=phone)
            serializer = RatingSerializer(all_comments,many=True)
            return Response({'all_comments':serializer.data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)