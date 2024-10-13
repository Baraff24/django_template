from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import STATUS_CHOICES, PENDING_COMPLETE_DATA, GENDER_CHOICES, NONE


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    Fields:
    - username, password, email (inherited)
    - first_name: User's first name
    - last_name: User's last name
    - telephone: Unique phone number for the user
    """
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
