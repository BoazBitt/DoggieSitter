from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from datetime import date
from django.urls import reverse



class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(validators=[MinLengthValidator(2)], max_length=50, blank=False)
    last_name = models.CharField(validators=[MinLengthValidator(2)], max_length=50, blank=False)
    email = models.CharField(validators=[MinLengthValidator(2)], max_length=50, blank=False)
    id = models.CharField(max_length=9,
                          validators=[MinLengthValidator(9)],
                          blank=False,
                          primary_key=True
    )
    gender = models.CharField(
        max_length=6,
        choices=[('male', 'male'), ('female', 'female')],
        blank=False,
    )
    date_of_birth = models.DateField(default=date.today)
    city = models.CharField(max_length=50,
                            blank=False,
    )
    neighborhood = models.CharField(max_length=50,
                                    blank=False,
    )
    street = models.CharField(max_length=50,
                              blank=False,
                              default="street and number"
    )
    aprt = models.CharField(max_length=50,
                            blank=False,
                            default="Aprt. number"
    )
    phone_number = models.CharField(max_length=10,
                                    validators=[MinLengthValidator(10)],
                                    blank=False,
    )
    is_doggiesitter = models.BooleanField()
    is_admin = models.BooleanField(default=False, blank=True, null=True)
    approved = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.user.username

class PostTerms(models.Model):
    author = models.TextField()
    title = models.IntegerField(primary_key=True)
    body = models.TextField()


    def __str__(self):
        return str(self.author) + '  |  terms'

    def get_absolute_url(self):
        return reverse('home')



class PostFeedback(models.Model):
    author = models.TextField(max_length=50)
    about = models.TextField()
    type = models.TextField()
    body = models.TextField()


    def __str__(self):
        return str(self.author) + '  |  Feedback'

    def get_absolute_url(self):
        return reverse('home')


class Trip(models.Model):
    trip_id = models.IntegerField(primary_key=True)
    dog_owner = models.CharField(max_length=50)
    dog = models.CharField(max_length=50)
    date = models.DateField(default=date.today)
    time = models.TimeField(blank=False)
    endtime = models.TimeField(blank=False)
    address = models.CharField(max_length=50, blank=True)
    comments = models.TextField(blank=True)
    duration = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    doggiesitter = models.TextField()
    is_taken = models.BooleanField(default=False, blank=True, null=True)
    is_done = models.BooleanField(default=False, blank=True, null=True)
    payment = models.CharField(
                                max_length=6,
                                choices=[('cash', 'cash'), ('credit', 'credit')],
                                default='cash',
                                blank=False,
                                )
    is_paid = models.BooleanField(default=False, blank=True, null=True)