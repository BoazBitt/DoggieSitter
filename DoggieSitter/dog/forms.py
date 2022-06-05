from django import forms
from .models import Dog


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ('name', 'age', 'gender', 'race', 'size', 'hobby', 'med')

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.isalpha():
            raise forms.ValidationError("Name must contain letters only")
        return name

    def clean_age(self):
        age = self.cleaned_data['age']
        if not age.isdigit():
            raise forms.ValidationError("Age must contain numbers only")

        return age

    def clean_race(self):
        race = self.cleaned_data['race']
        if not race.isalpha():
            raise forms.ValidationError("Race  must contain letters only")
        return race

