from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    name = models.CharField(max_length=100, default='User')
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    verified = models.BooleanField(default=False, verbose_name='Is Verified')

    @property
    def imageURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return  url
    

    def __str__(self):
        return self.username
    

class Text(models.Model):
    textfield = models.TextField()
    encrypted_text = models.TextField()
    key = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.textfield