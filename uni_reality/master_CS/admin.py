from django.contrib import admin

# Register your models here.
from .models import *

class UserAdmin(admin.ModelAdmin):
    model = User
    list_filter = ('is_superuser', 'type')
    list_display = ('type', 'name', 'surname', 'mail', 'is_superuser', 'is_admin')
    
admin.site.register(User, UserAdmin)