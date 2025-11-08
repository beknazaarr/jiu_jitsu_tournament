from django.urls import path
from . import views

app_name = 'athlete'

urlpatterns = [
    path('profile/<int:athlete_id>/', views.athlete_profile, name='profile'),
    path('category/<int:category_id>/', views.athlete_list_by_category, name='category_list'),
    path('schedule/<int:athlete_id>/', views.athlete_schedule, name='schedule'),
]