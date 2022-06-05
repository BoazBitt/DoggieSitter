import datetime
from datetime import date, time, datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import EmailValidator
from django.forms import SelectDateWidget
from .models import Accounts, PostTerms, Trip


class ExtendedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class AccountsProfileForm(forms.ModelForm):

    class Meta:
        model = Accounts
        fields = ('first_name', 'last_name', 'gender', 'date_of_birth', 'id', 'email', 'phone_number', 'city', 'neighborhood', 'street', 'aprt',  'is_doggiesitter')
        widgets = {
            'date_of_birth': SelectDateWidget(years=range(1902, date.today().year + 1)),
        }

    def clean_id(self):
        id = self.cleaned_data['id']
        if not id.isdigit():
            raise forms.ValidationError("ID must contain numbers only")
        if len(id) != 9:
            raise forms.ValidationError("ID number must be exactly 9 digits long")
        return id
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain numbers only")
        if len(phone_number) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits long")
        return phone_number
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        if age < 18:
            raise forms.ValidationError("Sorry, you have to be at least 18 years old in order to use our site's services.")
        if age > 120:
            raise forms.ValidationError("Sorry, you have to be at most 120 years old.")
        return date_of_birth
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain letters only")
        return first_name
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain letters only")
        return last_name
    def clean_email(self):
        email = self.cleaned_data['email']
        validator = EmailValidator()
        validator(email)
        return email
    def clean_city(self):
        city = self.cleaned_data['city']
        city1 = city.replace(" ", "")
        if not city1.isalpha():
            raise forms.ValidationError("City must contain letters only")
        if len(city) < 2:
            raise forms.ValidationError("City must be at least 2 letters long.")
        return city
    def clean_neighborhood(self):
        neighborhood = self.cleaned_data['neighborhood']
        if len(neighborhood) < 1:
            raise forms.ValidationError("Neighborhood must be at least 1 character long.")
        return neighborhood
    def clean_street(self):
        street = self.cleaned_data['street']
        if len(street) < 2:
            raise forms.ValidationError("Street must be at least 2 character long.")
        return street
    def clean_aprt(self):
        aprt = self.cleaned_data['aprt']
        if len(aprt) < 1:
            raise forms.ValidationError("Aprt must be at least 1 character long.")
        return aprt


class AccountChangeForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ('first_name', 'last_name', 'email', 'phone_number')

    def clean_email(self):
        email = self.cleaned_data['email']
        validator = EmailValidator()
        validator(email)
        return email



class TermsForm(forms.ModelForm):
    class Meta():
        model = PostTerms
        fields = ('author', 'title', 'body')

    def clean_author(self):
        author = self.cleaned_data['author']
        for i in User.objects.all():
            if author == i.username and not i.is_superuser:
                print("Only admins can post here.")
                raise forms.ValidationError("Only admins can post here.")
        return author
    def clean_title(self):
        title = self.cleaned_data['title']
        if not title.isdigit():
            print("Title must be numeric")
            raise forms.ValidationError("Title must be numeric")
        if title <= 0:
            print("Title number must be greater than 1.")
            raise forms.ValidationError("Title number must be greater than 1.")
        return title
    def clean_body(self):
        body = self.cleaned_data['body']
        return body


class TripForm(forms.ModelForm):
    class Meta():
        model = Trip
        fields = ('date', 'time', 'endtime', 'address', 'comments', 'payment')
        widgets = {
            'date': SelectDateWidget(years=range(date.today().year, date.today().year + 1)),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'endtime': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        today = date.today()
        if(date.month < today.month or (date.month == today.month and date.day < today.day) ):
                raise forms.ValidationError("This date already passed.")
        return date

    def clean_time(self):
        time = self.cleaned_data['time']
        date1 = date(1, 1, 1)
        time1 = datetime.combine(date1, time)
        timenow = datetime.combine(date1, datetime.now().time())
        duration = time1 - timenow
        try:
            date2 = self.cleaned_data['date']
        except:
            raise forms.ValidationError("Please check the date")
        today = date.today()
        if (date2.month == today.month and date2.day == today.day):
            if (duration.days < 0):
                raise forms.ValidationError("This time already passed.")
        return time

    def clean_address(self):
        address = self.cleaned_data['address']
        if(len(address) < 6):
                raise forms.ValidationError("Address is to short, please fill the full pickup address: city, neighborhood, street and aprt.")
        return address

    def clean_comments(self):
        comments = self.cleaned_data['comments']
        return comments

    def clean_endtime(self):
        endtime = self.cleaned_data['endtime']
        try:
            start = self.clean_time()
        except:
            raise forms.ValidationError("Please check the starting time.")
        date1 = date(1, 1, 1)
        endtime1 = datetime.combine(date1, endtime)
        start1 = datetime.combine(date1, start)
        duration = endtime1 - start1
        if (duration.days < 0):
            raise forms.ValidationError("The end time must be after the starting time.")
        return endtime

    def clean_payment(self):
        payment = self.cleaned_data['payment']
        return payment
