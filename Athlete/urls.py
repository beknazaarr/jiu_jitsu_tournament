from django.urls import path
from . import views

app_name = 'athlete'

urlpatterns = [
    # path('register/<int:tournament_id>/', views.athlete_registration, name='registration'),
    # path('success/<int:athlete_id>/', views.registration_success, name='registration_success'),
    path('profile/<int:athlete_id>/', views.athlete_profile, name='profile'),
]