from django.db import models
from django.utils.text import slugify  # Import slugify here
import uuid

# Choices for phone brands
BRAND_CHOICES = [
    ('Apple', 'Apple'),
    ('Samsung', 'Samsung'),
    ('Google', 'Google'),
    ('OnePlus', 'OnePlus'),
    ('Xiaomi', 'Xiaomi'),
    ('Realme', 'Realme'),
    ('Oppo', 'Oppo'),
    ('Vivo', 'Vivo'),
]

class Phone(models.Model):
    # Photo URLs
    front_pic = models.CharField(
        max_length=255,
        default="https://png.pngtree.com/element_our/20190528/ourmid/pngtree-cartoon-mobile-phone-image_1127554.jpg",
        null=True,
        blank=True
    )
    back_pic = models.CharField(
        max_length=255,
        default="https://png.pngtree.com/element_our/20190528/ourmid/pngtree-cartoon-mobile-phone-image_1127554.jpg",
        null=True,
        blank=True
    )

    # Introduce
    name = models.CharField(max_length=255)
    brand = models.CharField(
        max_length=255,
        choices=BRAND_CHOICES,
        default='Apple'  # Corrected default value to match choices
    )
    model = models.CharField(max_length=255)
    price = models.IntegerField()

    display_size = models.CharField(max_length=255, default="", null=True, blank=True)
    # Memory
    memory_internal = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)

    

    # Control
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    total_sold = models.IntegerField(default=0)
    
    
    available_count = models.IntegerField(default=10)
    is_available = models.BooleanField(default=True)
    discount_available = models.BooleanField(default=False)
    discount_persen = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['brand', 'model'], name="no_duplicate_model")
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify((self.name,self.brand,self.model,self.price,self.ram,))

        # Ensure slug uniqueness
        original_slug = self.slug
        queryset = Phone.objects.filter(slug=self.slug).exclude(id=self.id)
        if queryset.exists():
            self.slug = f"{original_slug}-{uuid.uuid4().hex[:6]}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (id={self.id})"

    def final_price(self):
        if not self.discount_available:
            return self.price - (self.price * self.discount_persen) / 100
        return self.price
    
    def avg_rating(self):
        total_comments = 0
        comments_sum = 0
        all_comments = self.comments.all()
        
        for single_comment in all_comments:
            if single_comment:
                comments_sum += single_comment.rating
                total_comments += 1
        
        if total_comments == 0:  # Avoid division by zero
            return 0
        
        ans = comments_sum / total_comments
        return round(ans, 1)  # Rounding to 1 decimal place

