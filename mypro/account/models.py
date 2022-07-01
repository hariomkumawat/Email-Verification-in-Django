from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE )
    auth_token = models.CharField(max_length=100)
    is_verifyed = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.user.username

class Reset(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE )
    forget_password_token = models.CharField(max_length=100 )
    created_at =models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.user.username
