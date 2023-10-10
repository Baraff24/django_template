from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import STATUS_CHOICES, PENDING_COMPLETE_DATA, GENDER_CHOICES, NONE, TYPE_OF_USER_CHOICES, PATIENT


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    The default Django user model has the following fields:
    - username
    - password
    - email
    """
    type_of_user = models.CharField(max_length=20, choices=TYPE_OF_USER_CHOICES, default=PATIENT)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING_COMPLETE_DATA)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=NONE)
    age = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    domicile = models.CharField(max_length=50, blank=True, null=True)
    education = models.CharField(max_length=50, blank=True, null=True)
    university = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    socio_economic_status = models.CharField(max_length=50, blank=True, null=True)
    self_harmful_thoughts = models.IntegerField(blank=True, null=True)
    n_exercises = models.IntegerField(blank=True, null=True)
    n_daily_questions = models.IntegerField(blank=True, null=True)
    n_baseline = models.IntegerField(default=1)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' - ' + self.email
