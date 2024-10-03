

from django.urls import path
from . import views

urlpatterns = [
     path('all_products/',views. GetALLPhoneAPIView.as_view(), name='all_products'),
     path('search/',views. PhoneSearchView.as_view(), name='phone-search'),
    # to add any phone in the data base clint user can not do it
    path('<str:brand>/<str:lp>/<str:hp>/', views.GetPhoneAPIView.as_view(), name='GetPhone'),
    # to fillter items brand name,low price ,high price
    # path('<int:id>/', views.GetPhoneWithIdAPIView.as_view(), name='GetPhoneWithId'),
    # to get a single phone
    path('popular/', views.GetPopular_phone.as_view(), name='GetPopular_phone'),
    # to get poular phone
    path('latest/', views.latest_phone.as_view(), name='latest_phone'),
    # to get new phines
]
