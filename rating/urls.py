from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.AddRatingView.as_view(), name='AddRatingView'),
    path('get/<int:product_id>/', views.Get_comments_for_a_PhoneWithIdAPIView.as_view(), name='get_comments'),
   
]