from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()

"""
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "password",
        "phone",
        "email",
        "first_name",
        "last_name",
        "role",
    )
    list_filter = ("username", "email", "phone")
    list_editable = (
        "username",
        "password",
        "phone",
        "email",
        "first_name",
        "last_name",
        "role",
    )
"""