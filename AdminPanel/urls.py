from django.urls import path
from . import views

urlpatterns = [
     path('phone/', views.PhoneAPIView.as_view(), name='phone-add'),
   
]