

from django.urls import path
from . import views

urlpatterns = [
    path('', views.getwish_List.as_view(), name='wish'),
    # to get all the with item of a user
    path('add/<int:id>/', views.add_to_wish_List.as_view(), name='wish-add'),
    # to add an item in wish list it will take the item id 
   
]
