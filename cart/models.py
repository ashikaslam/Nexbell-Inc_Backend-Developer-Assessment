from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from mobilephone.models import Phone


class Cart(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE,related_name='my_cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"Cart for {self.user.name} (ID: {self.id})"
    def in_total(self):
        items = self.items.all()
        total = 0
        for i in items:total += i.price()
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Phone, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart {self.cart.id}"
    def price(self):return self.product.final_price()*self.quantity

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart','product'],name="no_dupli_cart_item")
        ]
