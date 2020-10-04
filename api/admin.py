from django.contrib import admin
from . import models


@admin.register(models.UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "full_name",
        "email",
        "date_joined",
        "last_login",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "is_superuser",
        "date_joined",
        "last_login",
    )
    fieldsets = (
        (
            None,
            {"fields": ("username", "password", "email", ("first_name", "last_name"),)},
        ),
        ("User Statuses", {"fields": ("is_superuser", "is_staff", "is_active",)}),
        ("Permissions & Groups", {"fields": ("user_permissions", "groups",)}),
        ("Dates", {"fields": ("date_joined", "last_login",)}),
    )


@admin.register(models.TimeModel)
class TimeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "time",
        "dnf",
        "penalty",
        "comment",
        "created",
    )


@admin.register(models.CheckUsername)
class CheckUsernameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "created",
    )


@admin.register(models.CheckEmail)
class CheckEmailAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "created",
    )

