from django.contrib import admin
from . models import User,Email_varification
# Register your models here.


class user_admin(admin.ModelAdmin):
   
    list_display =['email','id']
admin.site.register(User,user_admin)

admin.site.register(Email_varification)
