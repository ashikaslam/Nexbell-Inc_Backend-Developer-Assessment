from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_my_cart.as_view(), name='cart'),
    # to get all the with item of a user
    path('add/<int:id>/', views.add_to_cart.as_view(), name='add_to_cart'),
    # to add an item in wish list it will take the item id 
    path('increase/<int:id>/', views.increase_quantity.as_view(), name='increase-quantity'),
    path('decrease/<int:id>/', views.decrease_quantity.as_view(), name='decrease-quantity'),
    path('remove_cart_tiem/<int:id>/', views.remove_cart_item.as_view(), name='remove_cart_item'),
]