from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Tournament
from Category.models import Category
from Athlete.models import Athlete


class TournamentListView(ListView):
    """Список всех турниров"""
    model = Tournament
    template_name = 'tournament/tournament_list.html'
    context_object_name = 'tournaments'
    
    def get_queryset(self):
        return Tournament.objects.filter(is_active=True)


class TournamentDetailView(DetailView):
    """Детальная информация о турнире"""
    model = Tournament
    template_name = 'tournament/tournament_detail.html'
    context_object_name = 'tournament'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.get_object()
        
        # Добавляем категории и количество участников
        context['categories'] = Category.objects.filter(
            tournament=tournament
        ).prefetch_related('athletes')
        
        context['total_athletes'] = Athlete.objects.filter(
            tournament=tournament,
            is_active=True
        ).count()
        
        return context


def tournament_categories_view(request, pk):
    """Список категорий турнира с участниками"""
    tournament = get_object_or_404(Tournament, pk=pk, is_active=True)
    categories = Category.objects.filter(tournament=tournament).prefetch_related('athletes')
    
    # Группируем спортсменов по категориям
    categories_data = []
    for category in categories:
        athletes = category.athletes.filter(is_active=True).order_by('last_name', 'first_name')
        categories_data.append({
            'category': category,
            'athletes': athletes,
            'count': athletes.count()
        })
    
    context = {
        'tournament': tournament,
        'categories_data': categories_data,
    }
    
    return render(request, 'tournament/tournament_categories.html', context)


def tournament_schedule_view(request, pk):
    """Расписание турнира"""
    tournament = get_object_or_404(Tournament, pk=pk, is_active=True)
    
    from Schedule.models import Schedule
    schedules = Schedule.objects.filter(
        match__grid__category__tournament=tournament
    ).select_related(
        'match__athlete1', 
        'match__athlete2',
        'match__grid__category'
    ).order_by('scheduled_time', 'mat_number')
    
    # Группируем по матам
    mats = {}
    for schedule in schedules:
        mat_num = schedule.mat_number
        if mat_num not in mats:
            mats[mat_num] = []
        mats[mat_num].append(schedule)
    
    context = {
        'tournament': tournament,
        'mats': dict(sorted(mats.items())),
    }
    
    return render(request, 'tournament/tournament_schedule.html', context)