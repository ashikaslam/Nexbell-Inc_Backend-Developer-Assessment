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





from . import models
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Address
from .serializers import AddressSerializer
from . import serializers





class Place_order(APIView):  # 3
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        try:
            user = request.user
            my_cart = user.my_cart
            all_items = my_cart.items.all()
            if len(all_items)<1:return Response(status=status.HTTP_400_BAD_REQUEST)
            current_adress = user.my_address
            if not current_adress:return Response(status=status.HTTP_400_BAD_REQUEST)
            oder_adress = models.OrderAddress.objects.create(
                 name =current_adress.name,
                 phone = current_adress.phone,
                 alt_phone_number =current_adress.alt_phone_number,
                 country = current_adress. country,
                 city = current_adress.city ,
                 area = current_adress. area ,
                 address = current_adress. address , )
            if not oder_adress:return Response(status=status.HTTP_400_BAD_REQUEST)
           
            total_price = my_cart.in_total()
            current_order = models.Order.objects.create(user=user,price=total_price,address=oder_adress)

            for single_item in all_items:
                    models.OrderedItem.objects.create(
                    price=single_item.product.final_price(),
                    order =current_order,
                    quantity=single_item.quantity,
                    image = single_item.product.front_pic,
                    product_id=single_item.product.id,
                    name=single_item.product.name
                    )
            for single_item in all_items:single_item.delete()
                    
            return Response(status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



class AddressCreateView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            addr = serializer.save()
            addr.user = request.user
            addr.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class get_of_a_order_AddressCreateView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    def get(self, request,order_id): # this is to get addredd for a order
        try:
            print(order_id)
            if not models.Order.objects.filter(id=order_id).exists():return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            order =models.Order.objects.get(id=order_id)
            user = request.user
            if (not user == order.user) and (not request.user.is_staff):return Response(status=status.HTTP_401_UNAUTHORIZED)
            address = models.Order.objects.get(id=order_id).address
            serializer = serializers.AddressSerializer(address, many=False)
            return Response({'address': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetMyOrder(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            # Assuming `my_orders` is a reverse relationship
            my_orders = user.my_orders.all()  # Add .all() to get the queryset
            results = []

            for single_order in my_orders:
                if single_order.status!='pending':continue
                order_items = single_order.items.all()  # Assuming `items` is a related manager
                total_price = single_order.price
                order_date = single_order.created_at
                payment_status = single_order.payment_status
                order_status = single_order.status
                order_id= single_order.id
                serializer = serializers.OrderedItemSerializer(order_items, many=True)
                results.append( {'order_status':order_status,'order_id':order_id, "time": order_date, 'payment_status' :payment_status, "in_total": total_price, 'all_items': serializer.data})
                
            return Response({'all_orders': results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    


class purchase_history(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            # Assuming `my_orders` is a reverse relationship
            my_orders = user.my_orders.all()  # Add .all() to get the queryset
            results = []

            for single_order in my_orders:
                if single_order.status!='complete':continue
                order_items = single_order.items.all()  # Assuming `items` is a related manager
                total_price = single_order.price
                order_date = single_order.created_at
                payment_status = single_order.payment_status
                order_status = single_order.status
                order_id= single_order.id
                serializer = serializers.OrderedItemSerializer(order_items, many=True)
                results.append( {'order_status':order_status,'order_id':order_id, "time": order_date,  'payment_status' :payment_status, "in_total": total_price, 'all_items': serializer.data})
                
            return Response({'all_orders': results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    

# codr for payment process

from django.shortcuts import render,redirect
from django.http import HttpResponse
import random
import string
from sslcommerz_lib import SSLCOMMERZ 
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
def generate_transaction_id(length=15):
    characters = string.ascii_letters + string.digits
    transaction_id = ''.join(random.choice(characters) for _ in range(length))
    return transaction_id
@csrf_exempt
def f(request):
    return render(request,'fail.html')
@csrf_exempt
def purchase(request,order_id):
    order = models.Order.objects.get(id=order_id)
    order.payment_status='paid'
    order.save()
    return render(request,'success.html')

def pay(request,user_id,order_id):

    try:
        try:
            order = models.Order.objects.get(id=order_id)
            user = User.objects.get(id=user_id)
            if order.user==user:
                amount_in_total = order.price
                if order.payment_status=='paid':return redirect(reverse('fail'))
            else: 
                print("helool xyc")
                return redirect(reverse('fail'))
        except Exception as e:return redirect(reverse('fail'))
            

        settings = {'store_id':'djang6694103d32b98','store_pass':'djang6694103d32b98@ssl','issandbox':True}
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = amount_in_total
        post_body['currency'] = "BDT"
        post_body['tran_id'] = "12345"
        post_body['success_url'] =f"http://127.0.0.1:8000/order/purchase/{order_id}/"
        post_body['fail_url'] = "http://127.0.0.1:8000/order/f/"
        post_body['cancel_url'] = "http://127.0.0.1:8000/order/f/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = "aslam"
        post_body['cus_email'] = "test@test.com"
        post_body['cus_phone'] = "01700000000"
        post_body['cus_add1'] = "customer address"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"


        response = sslcz.createSession(post_body) # API response
        print(response)
        # Need to redirect user to response['GatewayPageURL']
        return redirect(response['GatewayPageURL'])
    except Exception as e:return redirect(reverse('fail'))

