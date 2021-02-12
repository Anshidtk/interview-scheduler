from django.contrib import admin
from .models import Role, Profile, AvailableTimes
# Register your models here.
admin.site.register(Role)
admin.site.register(Profile)
admin.site.register(AvailableTimes)