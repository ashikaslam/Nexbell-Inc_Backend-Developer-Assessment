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

from .import serializers
from . import models
from cart.models import Cart
#from . import Utility_function
#from extra_fruction import problem_solver


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
User = get_user_model()
from . import Utility_function




class UserSignupView(APIView):  # 3
    serializer_class = serializers.UserSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            otp = Utility_function.generate_otp()
            token1 = Utility_function.generate_token()
            token2 = Utility_function.generate_token()
            email = serializer.validated_data['email']
            Email_varification_obj = models.Email_varification.objects.create(
                email=email, otp=otp, token1=token1, token2=token2

            )
            user = serializer.save()  # This internally calls create() with validated data
            if user:my_cart = Cart.objects.create(user=user)
            Utility_function.send_otp_for_registration(
                email, otp)
            # .........................X.............
            return Response({'message': 'go for the otp check',
                             'email': email, 'token1': token1, 'token2': token2,
                             "status": 1
                             }, status=status.HTTP_200_OK)
        

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)





class Varifi_otp_(APIView):  # 2
    serializer_class = serializers.otp_taker

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            token1 = serializer.validated_data['token1']
            token2 = serializer.validated_data['token2']
            Email_varification_obj = models.Email_varification.objects.filter(
                email=email, otp=otp, token1=token1, token2=token2).first()

            if Email_varification_obj and Email_varification_obj.is_otp_valid:
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
                Refresh = RefreshToken.for_user(user)
                profile=user.profile
                # this line not for production just for testing
                login(request,  user)
                return Response({'message': 'registration successful.', 
                                 'user_id':  user.id, 
                                 "profile_id":profile.id,
                                 "profile_picture": profile.profile_picture,
                                 "access": str(Refresh.access_token), 
                                 "status": 1,
                                 'refresh': str(Refresh)
                                 }, status=status.HTTP_200_OK)

            else:
                return Response({"error": "otp is invalied", "status": 0}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)





class User_login(APIView):  # 4
    serializer_class = serializers.LoginSerializer

    def post(self, request):

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            authenticated_user = authenticate(
                username=email, password=password)
            if authenticated_user:
                Refresh = RefreshToken.for_user(authenticated_user)
            
                # this line not for production just for testing
                login(request, authenticated_user)
                return Response({'message': 'registration successful.', 
                                 'user_id': authenticated_user.id, 
                                 "access": str(Refresh.access_token), 
                                 "status": 1,
                                 'refresh': str(Refresh)
                                 }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "your email or passwrod is incorrect", "status": 0}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class Logout(APIView):  # 8
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.logoutSerializer

    def post(self, request):
        logout(request)  # this line for testing not for production
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data['refresh_token']
                RefreshToken(refresh_token).blacklist()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)


