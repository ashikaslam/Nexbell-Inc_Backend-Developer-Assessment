

from django.urls import path
from . import views

urlpatterns = [
    path('placeoder/', views.Place_order.as_view(), name='Place_order'),
    path('get_my_orders/', views.GetMyOrder.as_view(), name='get_my_order'),
    path('purchase_history/', views.purchase_history.as_view(), name='purchase_history'),
    path('addresses/', views.AddressCreateView.as_view(), name='address-create'),
    path('addresses_get/<int:order_id>/', views.get_of_a_order_AddressCreateView.as_view(), name='get_of_a_order_AddressCreateView'),
    path('pay/<int:user_id>/<int:order_id>/', views.pay,name='pay'),
    path('f/', views.f,name='fail'),
    path('purchase/<int:order_id>/', views.purchase),
]
