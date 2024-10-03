from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Address)
admin.site.register(models.OrderAddress)
admin.site.register(models.Order)
admin.site.register(models.OrderedItem)