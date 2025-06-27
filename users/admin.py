from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone_number", "country")
    list_filter = ("email", "phone_number", "country")
    search_fields = ("email", "phone_number", "country")
