from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Role(models.Model):
    role_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.role_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return str(self.user)

class AvailableTimes(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    available_time_from = models.DateTimeField(blank=True,null=True)
    available_time_to = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return str(self.user)