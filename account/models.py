from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete = models.CASCADE)
    phone_no = models.CharField(max_length=120, default="")
    address = models.CharField(max_length=120, default="")
    gender = models.CharField(max_length=120, default="")
    date_of_birth = models.CharField(max_length=120, default="")
    hashcode = models.CharField(max_length=120, default="")
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)