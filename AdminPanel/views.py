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
from mobilephone.serializers import PhoneSerializer_to_add
from mobilephone.models import Phone

import requests


# product manage ment.................................
import os
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
load_dotenv()





def upload_image_to_imgbb(file):
    try:
        api_key =os.getenv('imagebb_api_key')
        api_url = f"https://api.imgbb.com/1/upload?key={api_key}"

        # Prepare the file for the request (ensure it is read as binary data)
        files = {'image': (file.name, file.read(), file.content_type)}

        # Post the file to ImgBB
        response = requests.post(api_url, files=files)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                image_url = data['data']['url']
                return image_url
        return None
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None







@csrf_exempt

class PhoneAPIView(APIView):  
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PhoneSerializer_to_add

    def post(self, request, *args, **kwargs):
        try:
            # Only staff users can perform this action
            if not request.user.is_staff:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            # Get images from the request
            front_img = request.FILES.get('front_img')
            back_img = request.FILES.get('back_img')

            # Remove images from the data before saving
            data = request.data.copy()
            data.pop('front_img', None)
            data.pop('back_img', None)

            # Serialize and validate the data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            current_phone = serializer.save()

            # Upload the images and update the model with the image URLs
            if front_img:
                front_img_url = upload_image_to_imgbb(front_img)
                if  front_img_url:  current_phone.front_pic = front_img_url

            if back_img:
                back_img_url = upload_image_to_imgbb(back_img)
                if back_img_url: current_phone.back_pic = back_img_url

            current_phone.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(f"Error in PhoneAPIView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request):
        try:
            product_id = request.GET.get('product_id')
            if not request.user.is_staff:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            Phone.objects.get(id=product_id).delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Adding the put method to edit a phone
    def put(self, request):
        try:
            if not request.user.is_staff:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            product_id = request.GET.get('product_id')
            if not Phone.objects.filter(id=product_id).exists():return Response(status=status.HTTP_404_NOT_FOUND)
            phone= Phone.objects.get(id=product_id)

            # Get images from the request
            front_img = request.FILES.get('front_img')
            back_img = request.FILES.get('back_img')

            # Remove images from the data before saving
            data = request.data.copy()
            data.pop('front_img', None)
            data.pop('back_img', None)
            # Serialize and validate the data
            serializer = self.serializer_class(phone,data=data, partial=False)
            serializer.is_valid(raise_exception=True)
            updated_phone = serializer.save()
            
            # Upload the images and update the model with the image URLs
            if front_img:
                front_img_url = upload_image_to_imgbb(front_img)
                if  front_img_url:  updated_phone.front_pic = front_img_url

            if back_img:
                back_img_url = upload_image_to_imgbb(back_img)
                if back_img_url: updated_phone.back_pic = back_img_url

            updated_phone.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



