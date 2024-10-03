from django.db import models
from django.contrib.auth import get_user_model
from mobilephone.models import Phone  # Assuming the Phone model is related

User = get_user_model()

class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 - Very Bad'),
        (2, '2 - Bad'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE,related_name='comments')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    edit_date = models.DateTimeField(auto_now=True)  # Automatically updates on each save

    class Meta:
        unique_together = ('user', 'phone')  # Prevents duplicate reviews from the same user for the same phone

   
