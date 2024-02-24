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
    

class File(models.Model):
    original_file = models.FileField(upload_to='files/original/')  # Field for storing the original file
    encrypted_file = models.FileField(upload_to='files/encrypted/')  # Field for storing the encrypted file
    key = models.CharField(max_length=255)  # Field for storing the encryption key
    read = models.BooleanField(default=False)  # Field for marking if the file has been read
    user_name = models.CharField(max_length=255, null=True, blank=True)  # Field for storing the username or "for everyone"
    date = models.DateTimeField(auto_now_add=True)  # Automatic date field

    def __str__(self):
        return f"File: {self.original_file.name}"
    

class Image(models.Model):
    original_file = models.ImageField(upload_to='Original_Image', blank=True, null=True) # Field for storing the original file
    encrypted_file = models.ImageField(upload_to='Steganographed_Image', blank=True, null=True) # Field for storing the encrypted file
    message = models.CharField(max_length=1000, null=True, blank=True)  # Field for storing the encryption key

    key = models.CharField(max_length=255)  # Field for storing the encryption key
    read = models.BooleanField(default=False)  # Field for marking if the file has been read
    user_name = models.CharField(max_length=255, null=True, blank=True)  # Field for storing the username or "for everyone"
    date = models.DateTimeField(auto_now_add=True)  # Automatic date field

    def __str__(self):
        return f"File: {self.original_file.name}"