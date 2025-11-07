from django.urls import path
from . import views

app_name = 'grid'

urlpatterns = [
    path('category/<int:category_id>/', views.grid_view, name='view'),
    path('category/<int:category_id>/generate/', views.generate_grid, name='generate'),
    path('match/<int:match_id>/update/', views.update_match_result, name='update_result'),
]