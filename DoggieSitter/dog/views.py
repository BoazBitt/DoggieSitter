from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.views import View
from .forms import DogForm
from .models import Dog


class AddDog(View):
    def get(self, request, user_id):
        form = DogForm()
        return render(request, 'AddDog.html', {'form_user': form, 'ok?': 'yes!'})

    def post(self, request, user_id):
        form = DogForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            tempdog1 = Dog.objects.create(
                # dog_id = Dog.objects.count() + 1,
                owner=user,
                name=form.cleaned_data['name'],
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                race=form.cleaned_data['race'],
                size=form.cleaned_data['size'],
                hobby=form.cleaned_data['hobby'],
                med=form.cleaned_data['med']
            )
            try:
                tempdog1.save()
            except:
                pass
            return render(request, 'home.html', {'ok?': 'form is valid!'})
        return render(request, 'AddDog.html', {'form_user': form, 'ok?': 'form is not valid!'})


