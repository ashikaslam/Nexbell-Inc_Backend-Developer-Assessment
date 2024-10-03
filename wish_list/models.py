from django.db import models
from mobilephone. models import Phone
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_wish')
    phone = models.ForeignKey(Phone,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','phone'], name='unique_user_phone')
        ]
        ordering = ['-id']  # This orders by 'id' by default
   