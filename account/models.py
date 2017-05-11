from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.

class Profile(models.Model):
    # we start linking the User Profile to the default AUTH_USER_MODEL. In case this variable
    # is not specified in the settings file, it will default to the "auth.User" object
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    slug = models.SlugField(max_length=30, unique=True)
    about = models.TextField(max_length=1000)

    def get_absolute_url(self):
        return reverse('dj-auth:public_profile', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('dj-auth:profile_update')

    def __str__(self):
        return self.user.get_username()
