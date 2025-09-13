from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    address = models.CharField(max_length=120, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    USER_ROLE = (
        ('admin', 'Admin'),
        ('customer', 'Mijoz')
    )

    role = models.CharField(max_length=20, choices=USER_ROLE, default='customer')

    def __str__(self):
        return f"{self.username} - {self.role}"
