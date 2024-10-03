from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Address(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE,blank=True, null=True,related_name='my_address')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    alt_phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    address = models.TextField()
    
    
    

class OrderAddress(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    alt_phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    address = models.TextField()
    




class Order(models.Model):
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('complete', 'Complete'),
    ('canceled', 'Canceled'),
]

    
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]
    user =models.ForeignKey(User, on_delete=models.CASCADE,related_name='my_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    address = models.OneToOneField(OrderAddress, on_delete=models.CASCADE,blank=True, null=True)
    
    class Meta:
         ordering = ['-id']  # This orders by 'id' by default



class OrderedItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField()
    name=models.CharField(max_length=255,null=True, blank=True,default=None)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    image=models.CharField(max_length=255,null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order','product_id'],name="no_dupli_order_item")
        ]
   


