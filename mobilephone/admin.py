from django.contrib import admin
from . import models
# Register your models here.



class Phone_admin(admin.ModelAdmin):
    # prepopulated_fields={'slug':('name','brand','model','price','ram',)}
    list_display =['name','id']




admin.site.register(models.Phone,Phone_admin)
