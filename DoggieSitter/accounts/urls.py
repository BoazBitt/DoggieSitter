# accounts/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views, admin
from .views import ShowFeedback


urlpatterns = [
    path(" ", views.go_home, name="home"),
    path("signup/", views.SignUpView, name="signup"),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('gallery', TemplateView.as_view(template_name='gallery.html'), name='gallery'),
    path("user_info/", views.GetAccounts, name="user_info"),
    path('admin_actions/make_admin', admin.make_new_admin, name='admin_actions/make_admin'),
    path("admin_actions/remove_admin", admin.delete_admin, name="admin_actions/remove_admin"),
    path('admin_actions/delete_user', admin.delete_user, name='admin_actions/delete_user'),
    path('admin_actions/approve_doggiesitter', admin.approve_doggiesitter, name='admin_actions/approve_doggiesitter'),
    path('admin_actions/', views.SearchUserByID, name='admin_actions'),
    path('change/<user_id>', views.changeAccount.as_view(), name='changeinfo'),
    path('change_password/<un>', views.GetUsername, name='change_password'),
    path('change_password2/', views.ChangePassword, name='change_password2'),
    path('Terms', views.Terms, name="Terms"),
    path('Feedback', views.Feedback, name="Feedback"),
    path('ShowFeedback', ShowFeedback.as_view(), name="ShowFeedback"),
    path('Add', views.Add, name="Add"),
    path('vet_map/<un>', views.Vet_Map, name="vet_map"),
    path('parks/<un>', views.Parks, name="parks"),
    path('DogPage/<user_id>', views.DogPage.as_view(), name='DogPage'),
    path("addtrip/<str:usr>", views.AddTrip, name="addtrip"),
    path("takentrip/<usr>", views.TakenTrips, name="taken"),
    path("alltrips/<usr>", views.AllTrips, name="alltrips"),
    path("taketrip/<tr_id>", views.TakeTrip, name="taketrip"),
    path('dogs', views.dogs, name="dogs"),
    path("deposit_complete/", views.DepositComplete, name="deposit_complete/"),
    path("upcoming_trips/<usr>", views.UpcomingTrips, name="upcoming_trips"),
    path("RateDoggie/<usr>", views.RateDoggie, name="Rate"),
    path("checkpayment/", views.CheckPayment, name="checkpayment"),
    path("doggie_request/", views.DoggieRequest, name="doggie_request"),
    path("deleteDog/<usr> <name>", views.DeleteDog, name="deleteDog"),
    path("deletetrip/<tr_id> <usr>", views.DeleteTrip, name="deletetrip"),

]
