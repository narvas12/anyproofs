from django.contrib import admin
from .models import CustomUser, Transaction

# Register your models here.


@admin.register(CustomUser)
class UserManager(admin.ModelAdmin):
    pass
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']

@admin.register(Transaction)
class UserManager(admin.ModelAdmin):
    pass
    list_display = ['created_at', 'reciever', 'amount']