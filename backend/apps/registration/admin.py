from django.contrib import admin

from apps.registration.models import (
    Interest,
    UserProfile,
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)
    raw_id_fields = ("user",)


class InterestAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    raw_id_fields = ("users",)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Interest, InterestAdmin)
