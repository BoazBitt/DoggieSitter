from django.urls import path

from dog import views

urlpatterns = [

    path('AddDog/<user_id>', views.AddDog.as_view(), name='Adding'),
]
