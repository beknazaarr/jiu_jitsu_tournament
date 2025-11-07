from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tournaments/', include('Tournament.urls')),
    path('athletes/', include('Athlete.urls')),
    path('grids/', include('TournamentGrid.urls')),
    path('', RedirectView.as_view(url='/tournaments/', permanent=False)),
]

# Настройка заголовков админки
admin.site.site_header = "Турнирная система джиу-джитсу"
admin.site.site_title = "Админ-панель турниров"
admin.site.index_title = "Управление турнирами"