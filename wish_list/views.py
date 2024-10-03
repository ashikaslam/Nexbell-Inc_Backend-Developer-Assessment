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


from mobilephone. models import Phone
from wish_list. models import Wish
from django.contrib.auth import get_user_model
from mobilephone.serializers import PhoneSerializer
User = get_user_model()




class add_to_wish_List(APIView):  # it can add or delete wish item
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,id): # this is the if of a phone object
        try:
            user = request.user
            phone =  Phone.objects.get(id=id)
            if Wish.objects.filter(user=user,phone=phone).exists():
                Wish.objects.get(user=user,phone=phone).delete()
                return Response({"status": 1},status=status.HTTP_200_OK)
            Wish.objects.create(user=user,phone=phone)
            return Response({ "status": 1},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




class getwish_List(APIView):  # 3
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            print(user)
            wish_list = user.my_wish.all()
            print(wish_list)
            all_obj=[]
            for i in wish_list:all_obj.append(i.phone)
            serializer = PhoneSerializer(all_obj,many=True)
            return Response({'all_phones':serializer.data})
           
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)