from datetime import date
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Dog(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(primary_key=True,validators=[MinLengthValidator(2)], max_length=50, blank=False)
    age = models.CharField(max_length=2,
                           validators=[MinLengthValidator(1)],
                           blank=False,
                           )
    gender = models.CharField(
        max_length=6,
        choices=[('male', 'male'), ('female', 'female')],
        blank=False,
    )
    race = models.CharField(validators=[MinLengthValidator(2)], max_length=50, blank=False)
    size = models.CharField(
        max_length=7,
        choices=[('small', 'small'), ('average', 'average'), ('big', 'big')],
        blank=False,
    )
    hobby = models.CharField(validators=[MinLengthValidator(2)], max_length=50, blank=False)
    med = models.CharField(validators=[MinLengthValidator(2)], max_length=50, blank=False)

    def __str__(self):
        return self.owner.username
