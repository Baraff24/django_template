from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import STATUS_CHOICES, PENDING_COMPLETE_DATA, GENDER_CHOICES, NONE


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    The default Django user model has the following fields:
    - username
    - password
    - email
    """
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default=PENDING_COMPLETE_DATA)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=NONE)

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.last_name, self.email)
