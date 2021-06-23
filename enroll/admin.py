from django.contrib import admin
from.models import Profile
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','profile_img','auth_token','is_verify','create_at']