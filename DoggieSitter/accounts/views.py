# accounts/views.py
import json
from datetime import date, datetime
from pprint import pprint
from time import sleep
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from django import forms
from .forms import ExtendedUserCreationForm, AccountsProfileForm, AccountChangeForm, TermsForm, TripForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Accounts, PostTerms, PostFeedback, Trip
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
import googlemaps
from geopy.geocoders import Nominatim
from django.views.generic import ListView
from dog.models import Dog


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'password_success.html', {})


def SignUpView(request):
    pt = PostTerms.objects.all()
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = AccountsProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
        else:
            return render(request, 'registration/signup.html',
                          {'form': form, 'profile_form': profile_form, 'pt': pt, 'error': "Bad Data Please Try Again"})
    else:
        form = ExtendedUserCreationForm()
        profile_form = AccountsProfileForm()
    context = {'form': form, 'profile_form': profile_form, 'error': "Bad Data Please Try Again", 'pt': pt}
    return render(request, 'registration/signup.html', context)


def GetAccounts(request):
    acc = Accounts.objects.all()
    usr = User.objects.all()
    return render(request, 'user_info.html', {'acc': acc, 'usr': usr})


def SearchUserByID(request):
    if request.method == 'POST':
        us = Accounts.objects.filter(id=request.POST.get("search_id"))
        if (len(us) == 0):
            return render(request, 'search_result.html', {'us': 'empty'})
        if request.POST.get('adminac') == 'info':
            return render(request, 'search_result.html', {'us': us})
        else:
            usr = us[0].user.username
            if us[0].is_doggiesitter:
                taken = Trip.objects.filter(doggiesitter=usr)
                return render(request, 'UserActivity.html', {'trips': taken, 'doggiok': 'ok'})
            else:
                posted = Trip.objects.filter(dog_owner=usr)
                return render(request, 'UserActivity.html', {'trips': posted, 'ownerok': 'ok'})
    return render(request, 'admin_actions.html')


class changeAccount(View):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        if not user.is_superuser:
            account = Accounts.objects.get(user=user)
            form = AccountChangeForm(instance=account)
            return render(request, 'change.html', {'form_user': form, 'ok?': 'yes!'})
        else:
            return render(request, 'home.html', {'ok?': 'yes!'})

    def post(self, request, user_id):
        form = AccountChangeForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            account = Accounts.objects.get(user=user)
            account.first_name = form.cleaned_data['first_name']
            account.last_name = form.cleaned_data['last_name']
            account.email = form.cleaned_data['email']
            account.phone_number = form.cleaned_data['phone_number']
            account.save()
            return render(request, 'home.html', {'ok?': 'form is valid!'})
        return render(request, 'change.html', {'form_user': form, 'ok?': 'form is not valid!'})


def GetUsername(request, un):
    user = User.objects.get(username=un)
    return render(request, 'change_password.html', {'user': user})


def go_home(request, temp):
    return render(request, temp)


def ChangePassword(request):
    user = User.objects.get(username=request.POST.get("user_n"))
    if request.POST.get("new_pass1") == request.POST.get("new_pass2"):
        try:
            validate_password(request.POST.get("new_pass1"), user=user, password_validators=None)
            user.set_password(request.POST.get("new_pass1"))
            user.save()
            return render(request, 'pass_change_done.html', {'result_pass': "Password successfully changed."})
        except ValidationError as error:
            return render(request, 'change_password.html', {'error': error})
    else:
        return render(request, 'pass_change_done.html', {'result_pass': "The 2 passwords doesn't match."})


def Terms(request):
    term_form = TermsForm(request.POST)
    if request.method == 'POST' and not term_form.is_valid():
        try:
            post = PostTerms.objects.get(title=request.POST.get("title_name"))
        except Exception as e:
            post = PostTerms()
            post.body = request.POST.get("body_name")
            post.author = request.POST.get("author_name")
            post.title = request.POST.get("title_name")
            post.save()
            return render(request, 'home.html')

        post.title = request.POST.get("title_name")
        post.body = request.POST.get("body_name")
        post.author = request.POST.get("author_name")
        post.save()
        return render(request, 'home.html', {'Term': 'Try Worked'})
    else:
        pt = PostTerms.objects.all()
        return render(request, 'Terms.html', {'pt': pt})


def Add(request):
    pt = PostTerms.objects.all()
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = AccountsProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return render(request, 'home.html', {'add': 'done'})
        else:
            return render(request, 'registration/Add.html',
                          {'form': form, 'profile_form': profile_form, 'pt': pt,
                           'error': "Bad Data Please Try Again"})
    else:
        form = ExtendedUserCreationForm()
        profile_form = AccountsProfileForm()
    context = {'form': form, 'profile_form': profile_form, 'error': "Bad Data Please Try Again", 'pt': pt}
    return render(request, 'registration/Add.html', context)


def Vet_Map(request, un):
    check = User.objects.get(username=un)
    check2 = Accounts.objects.get(user=check)
    API_KEY = "Enter Your Goofle API"
    map_client = googlemaps.Client(API_KEY)
    app = Nominatim(user_agent="tutorial")

    location_name = "מרפאה וטרינרית, "
    location = ""

    for i in Accounts.objects.all():
        if str(i) == str(un):
            user = Accounts.objects.get(id=i.id)
            location_name += user.city
            location = app.geocode("Israel, " + str(user.city)).raw

    city = {'lat': location['lat'], 'lng': location['lon']}
    try:
        response = map_client.places(query=location_name)
        results = response.get('results')
    except Exception as e:
        print(e)
        return None
    location_data = []
    for i in results:
        location_data.append(i['geometry']['location'])
        (location_data[location_data.index(i['geometry']['location'])])['name'] = i['name']

        try:
            if i['opening_hours'].values() == True:
                (location_data[location_data.index(i['geometry']['location'])])['opening_hours'] = "Open"
            else:
                (location_data[location_data.index(i['geometry']['location'])])['opening_hours'] = "Close"
        except:
            pass

    return render(request, 'vet_map.html', {'location_data': location_data, 'city': city, 'ok?': 'yes!'})


def Feedback(request):
    if request.method == 'POST':
        post = PostFeedback()
        post.body = request.POST.get("body_name")
        post.author = request.POST.get("author_name")
        post.about = request.POST.get("about_id")
        post.type = request.POST.get("type")
        post.save()
        return render(request, 'home.html', {'ok?': 'post!'})
    else:
        pt = PostFeedback.objects.all()
        return render(request, 'Feedback.html', {'pt': pt, 'ok?': 'get!'})


class ShowFeedback(ListView):
    model = PostFeedback
    template_name = 'ShowFeedback.html'


class DogPage(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        mydog = Dog.objects.filter(owner=user).order_by('name')
        return render(request, 'DogPage.html', {'dogs': mydog, 'ok?': 'yes!'})


def Parks(request, un):
    API_KEY = "Enter Your Goofle API"
    map_client = googlemaps.Client(API_KEY)
    app = Nominatim(user_agent="tutorial")

    location_name = "Dog Park, "
    location = ""

    for i in Accounts.objects.all():
        if str(i) == str(un):
            user = Accounts.objects.get(id=i.id)
            location_name += user.city
            location = app.geocode("Israel, " + str(user.city)).raw

    city = {'lat': location['lat'], 'lng': location['lon']}

    try:
        response = map_client.places(query=location_name)
        results = response.get('results')
    except Exception as e:
        print(e)
        return None

    location_data = []
    for i in results:
        location_data.append(i['geometry']['location'])

        try:
            if i['opening_hours'].values() == True:
                (location_data[location_data.index(i['geometry']['location'])])['opening_hours'] = "Open"
            else:
                (location_data[location_data.index(i['geometry']['location'])])['opening_hours'] = "Close"
        except:
            pass
        try:
            (location_data[location_data.index(i['geometry']['location'])])['name'] = i['name']
        except:
            pass
        try:
            (location_data[location_data.index(i['geometry']['location'])])['rating'] = i['rating']
        except:
            pass
        try:
            (location_data[location_data.index(i['geometry']['location'])])['formatted_address'] = i[
                'formatted_address']
        except:
            pass

    return render(request, 'parks.html', {'location_data': location_data, 'city': city, 'ok?': 'yes!'})


def AddTrip(request, usr):
    if request.method == 'POST':
        trip = TripForm(request.POST)
        trips = Trip()
        if trip.is_valid():
            trips.trip_id = Trip.objects.count() + 1
            trips.dog_owner = usr
            trips.dog = request.POST.get('item_id')
            trips.date = trip.cleaned_data['date']
            trips.time = trip.cleaned_data['time']
            trips.endtime = trip.cleaned_data['endtime']
            trips.address = trip.cleaned_data['address']
            trips.comments = trip.cleaned_data['comments']
            trips.payment = trip.cleaned_data['payment']
            date1 = date(1, 1, 1)
            endtime1 = datetime.combine(date1, trips.endtime)
            start1 = datetime.combine(date1, trips.time)
            duration = endtime1 - start1
            trips.duration = duration.seconds / 3600
            trips.price = trips.duration * 30
            trips.save()
            if trips.payment == "credit":
                return render(request, 'checkpayment.html', {'trip': trips, 'ok?': 'post!'})
            return render(request, 'home.html', {'ok?': 'post!'})
        else:
            return render(request, 'addtrip.html', {'trip': trip, 'ok?': 'get!'})
    else:
        own = User.objects.get(username=usr)
        dogs = Dog.objects.filter(owner=own).values()
        result = [dog['name'] for dog in dogs]
        trip = TripForm()
        trip.dog = result
        return render(request, 'addtrip.html', {'trip': trip, 'ok?': 'get!', 'result': result})


def AllTrips(request, usr):
    trips = Trip.objects.all()
    my_trips = Trip.objects.filter(dog_owner=usr)
    return render(request, 'alltrips.html', {'trips': trips, 'my_trips': my_trips})


def dogs(request):
    all = Dog.objects.all()
    return render(request, 'dogs.html', {'all': all, 'ok?': 'yes'})


def TakeTrip(request, tr_id):
    if request.method == 'POST':
        trip = Trip.objects.get(trip_id=tr_id)
        own = User.objects.get(username=trip.dog_owner)
        dog = Dog.objects.get(owner=own, name=trip.dog)
        return render(request, 'taketrip.html', {'trip': trip, 'dog': dog, 'ok?': 'post'})
    return render(request, 'home.html', {'ok?': 'get'})


def DepositComplete(request):
    body = json.loads(request.body)
    trip = Trip.objects.get(trip_id=body['tripid'])
    trip.is_taken = True
    trip.doggiesitter = body['doggiesitter']
    trip.duration = trip.duration.to_decimal()
    trip.price = trip.price.to_decimal()
    trip.save()
    return render(request, 'taketrip.html', {'trip': trip})


def UpcomingTrips(request, usr):
    trips = Trip.objects.filter(doggiesitter=usr, is_done__in=[False])
    return render(request, 'upcoming_trips.html', {'trips': trips})


def RateDoggie(request, usr):
    list = []
    notall = Trip.objects.filter(dog_owner=usr, is_done__in=[True])
    all = Accounts.objects.filter(is_doggiesitter__in=[True], approved__in=[True])
    for i in notall.iterator():
        u = User.objects.get(username=i.doggiesitter)
        a = Accounts.objects.get(user=u)
        list.append(a)
    return render(request, 'RateDoggie.html', {'acc': set(list), 'ok': 'ok', 'all': all})


def CheckPayment(request):
    body = json.loads(request.body)
    trip = Trip.objects.get(trip_id=body['tripid'])
    trip.is_paid = True
    trip.duration = trip.duration.to_decimal()
    trip.price = trip.price.to_decimal()
    trip.save()
    return render(request, 'taketrip.html', {'trip': trip})


def TakenTrips(request, usr):
    trips = Trip.objects.filter(dog_owner=usr)
    if (request.method == 'POST'):
        if 'done' in request.POST:
            trip = Trip.objects.get(trip_id=request.POST.get('done'))
            trip.is_done = True
            trip.is_paid = True
            trip.duration = trip.duration.to_decimal()
            trip.price = trip.price.to_decimal()
            trip.save()
            return render(request, 'home.html')
        else:
            return render(request, 'TakenTrips.html', {'trips': trips})
    else:
        return render(request, 'TakenTrips.html', {'trips': trips})

def DoggieRequest(request):
    usr = Accounts.objects.filter(is_doggiesitter__in=[True], approved__in=[False])
    if request.method == "POST":
        return render(request, 'doggie_request.html', {'usr': usr, 'num': len(usr)})
    return render(request, 'home.html')


def DeleteDog(request, usr, name):
    if request.method == 'POST':
        own = User.objects.get(username=usr)
        dog = Dog.objects.get(name=name,owner=own)
        dog.delete()
        dogs = Dog.objects.filter(owner = own)
        return render(request,'DogPage.html',{'dogs': dogs})
    else:
        return render(request, 'DogPage.html')

def DeleteTrip(request, tr_id, usr):
    trip = Trip.objects.filter(trip_id=tr_id)
    trip.delete()
    trips = Trip.objects.all()
    my_trips = Trip.objects.filter(dog_owner=usr)
    return render(request, 'alltrips.html', {'trips': trips, 'my_trips': my_trips})
