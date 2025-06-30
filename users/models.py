from django.db import models
from django.contrib.auth.models import User as AuthUser


class Profile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
