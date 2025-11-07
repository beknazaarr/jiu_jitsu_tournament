from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AthleteRegistrationForm
from .models import Athlete
from Tournament.models import Tournament


def athlete_registration(request, tournament_id):
    """Регистрация спортсмена на турнир"""
    tournament = get_object_or_404(Tournament, pk=tournament_id, is_active=True)
    
    # Проверяем, открыта ли регистрация
    if not tournament.registration_open:
        messages.warning(request, 'Регистрация на этот турнир закрыта')
        return redirect('tournament:detail', pk=tournament_id)
    
    if request.method == 'POST':
        form = AthleteRegistrationForm(request.POST, tournament=tournament)
        
        if form.is_valid():
            athlete = form.save(commit=False)
            athlete.tournament = tournament
            athlete.save()
            
            messages.success(
                request, 
                f'Спортсмен {athlete.full_name} успешно зарегистрирован на турнир!'
            )
            return redirect('athlete:registration_success', athlete_id=athlete.id)
    else:
        form = AthleteRegistrationForm(tournament=tournament)
    
    context = {
        'form': form,
        'tournament': tournament,
    }
    
    return render(request, 'athlete/registration.html', context)


def registration_success(request, athlete_id):
    """Страница успешной регистрации"""
    athlete = get_object_or_404(Athlete, pk=athlete_id)
    
    context = {
        'athlete': athlete,
        'tournament': athlete.tournament,
    }
    
    return render(request, 'athlete/registration_success.html', context)


def athlete_profile(request, athlete_id):
    """Просмотр профиля спортсмена"""
    athlete = get_object_or_404(Athlete, pk=athlete_id, is_active=True)
    
    # Получаем матчи спортсмена
    from Match.models import Match
    matches = Match.objects.filter(
        models.Q(athlete1=athlete) | models.Q(athlete2=athlete)
    ).select_related('athlete1', 'athlete2', 'winner').order_by('match_number')
    
    # Статистика
    wins = matches.filter(winner=athlete, is_completed=True).count()
    total_matches = matches.filter(is_completed=True).count()
    
    context = {
        'athlete': athlete,
        'matches': matches,
        'wins': wins,
        'total_matches': total_matches,
    }
    
    return render(request, 'athlete/profile.html', context)