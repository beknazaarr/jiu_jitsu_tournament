from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .forms import AthleteRegistrationForm
from .models import Athlete
from Tournament.models import Tournament
from Match.models import Match


def athlete_profile(request, athlete_id):
    """Просмотр профиля спортсмена"""
    athlete = get_object_or_404(Athlete, pk=athlete_id, is_active=True)
    
    # Получаем матчи спортсмена
    matches = Match.objects.filter(
        Q(athlete1=athlete) | Q(athlete2=athlete)
    ).select_related(
        'athlete1', 'athlete2', 'winner', 'grid__category'
    ).order_by('match_number')
    
    # Статистика
    wins = matches.filter(winner=athlete, is_completed=True).count()
    losses = matches.filter(is_completed=True).exclude(winner=athlete).exclude(winner=None).count()
    total_matches = matches.filter(is_completed=True).count()
    
    # Предстоящие матчи
    upcoming_matches = matches.filter(is_completed=False)
    
    context = {
        'athlete': athlete,
        'matches': matches,
        'wins': wins,
        'losses': losses,
        'total_matches': total_matches,
        'upcoming_matches': upcoming_matches,
        'win_rate': (wins / total_matches * 100) if total_matches > 0 else 0,
    }
    
    return render(request, 'athlete/profile.html', context)


def athlete_list_by_category(request, category_id):
    """Список спортсменов в категории"""
    from Category.models import Category
    
    category = get_object_or_404(Category, pk=category_id)
    athletes = category.athletes.filter(is_active=True).order_by('last_name', 'first_name')
    
    context = {
        'category': category,
        'tournament': category.tournament,
        'athletes': athletes,
    }
    
    return render(request, 'athlete/category_list.html', context)


def athlete_schedule(request, athlete_id):
    """Расписание боёв спортсмена"""
    athlete = get_object_or_404(Athlete, pk=athlete_id, is_active=True)
    
    # Получаем матчи с расписанием
    from Schedule.models import Schedule
    
    schedules = Schedule.objects.filter(
        Q(match__athlete1=athlete) | Q(match__athlete2=athlete)
    ).select_related(
        'match__athlete1', 'match__athlete2', 'match__grid__category'
    ).order_by('scheduled_time')
    
    context = {
        'athlete': athlete,
        'schedules': schedules,
    }
    
    return render(request, 'athlete/schedule.html', context)