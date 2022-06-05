from django.contrib import admin
from django.shortcuts import render
from .models import Accounts, PostFeedback, Trip
from django.contrib.auth.models import User
from .models import PostTerms


def make_new_admin(request):
    user = User.objects.get(username=request.POST.get("selected_id"))
    for i in Accounts.objects.all():
        if str(i) == str(user):
            ac = Accounts.objects.get(id=i.id)
    ac.is_admin = True
    user.is_superuser = True
    user.is_staff = True
    user.save()
    ac.save()
    return render(request, 'successful_action.html', {'result': "Admin permissions was successfully granted."})


def delete_admin(request):
    user = User.objects.get(username=request.POST.get("selected_id"))
    for i in Accounts.objects.all():
        if str(i) == str(user):
            ac = Accounts.objects.get(id=i.id)
    ac.is_admin = False
    user.is_superuser = False
    user.is_staff = False
    user.save()
    ac.save()
    return render(request, 'successful_action.html', {'result': "Admin permissions was successfully denied."})

def delete_user(request):
    user = User.objects.get(username=request.POST.get("selected_id"))
    User.delete(user)
    return render(request, 'successful_action.html', {'result': "User deleted successfully."})

def approve_doggiesitter(request):
    user = User.objects.get(username=request.POST.get("selected_id"))
    for i in Accounts.objects.all():
        if str(i) == str(user):
            ac = Accounts.objects.get(id=i.id)
    ac.approved = True
    user.save()
    ac.save()
    return render(request, 'successful_action.html', {'result': "Doggiesitter was successfully approved."})


class NewAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'is_doggiesitter', 'approved']
    ordering = ['first_name', 'last_name']
    actions = [make_new_admin, delete_admin]


admin.site.register(Accounts, NewAdmin)
admin.site.register(PostTerms)
admin.site.register(PostFeedback)
admin.site.register(Trip)


