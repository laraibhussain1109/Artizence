from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_influencer = models.BooleanField(default=False)
    is_brand = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"