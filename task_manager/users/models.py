from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission


# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='auth_user_groups')
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='auth_user_permissions',
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def __str__(self):
        return self.get_full_name()
