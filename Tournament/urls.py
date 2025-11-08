from django.urls import path
from .views import (
    TournamentListView,
    TournamentDetailView,
    tournament_categories_view,
    tournament_schedule_view,
    tournament_results_view,
)

app_name = 'tournament'

urlpatterns = [
    path('', TournamentListView.as_view(), name='list'),
    path('<int:pk>/', TournamentDetailView.as_view(), name='detail'),
    path('<int:pk>/categories/', tournament_categories_view, name='categories'),
    path('<int:pk>/schedule/', tournament_schedule_view, name='schedule'),
    path('<int:pk>/results/', tournament_results_view, name='results'),
]