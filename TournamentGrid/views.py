from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import TournamentGrid
from .grid_generator import GridGenerator
from Category.models import Category


def grid_view(request, category_id):
    """Просмотр турнирной сетки категории"""
    category = get_object_or_404(Category, pk=category_id)
    
    try:
        grid = category.grid
        generator = GridGenerator(grid)
        bracket_structure = generator.get_bracket_structure()
        
        context = {
            'category': category,
            'tournament': category.tournament,
            'grid': grid,
            'bracket_structure': bracket_structure,
        }
        
        return render(request, 'tournament_grid/grid_view.html', context)
    
    except TournamentGrid.DoesNotExist:
        context = {
            'category': category,
            'tournament': category.tournament,
            'error': 'Турнирная сетка ещё не создана для этой категории'
        }
        return render(request, 'tournament_grid/grid_view.html', context)


@staff_member_required
def generate_grid(request, category_id):
    """Генерация турнирной сетки (только для администраторов)"""
    category = get_object_or_404(Category, pk=category_id)
    
    # Создаём или получаем сетку
    grid, created = TournamentGrid.objects.get_or_create(
        category=category,
        defaults={'grid_type': 'single_elimination'}
    )
    
    try:
        generator = GridGenerator(grid)
        matches_count = generator.generate_single_elimination()
        
        messages.success(
            request, 
            f'Сетка успешно сгенерирована! Создано {matches_count} поединков.'
        )
    except ValueError as e:
        messages.error(request, str(e))
    
    return redirect('grid:view', category_id=category_id)


@staff_member_required
def update_match_result(request, match_id):
    """Обновление результата матча"""
    from Match.models import Match
    
    if request.method == 'POST':
        match = get_object_or_404(Match, pk=match_id)
        
        # Получаем данные из формы
        winner_id = request.POST.get('winner')
        score1 = request.POST.get('score_athlete1', 0)
        score2 = request.POST.get('score_athlete2', 0)
        result_type = request.POST.get('result_type')
        
        # Обновляем матч
        if winner_id:
            from Athlete.models import Athlete
            match.winner = Athlete.objects.get(pk=winner_id)
        
        match.score_athlete1 = int(score1)
        match.score_athlete2 = int(score2)
        match.result_type = result_type
        match.is_completed = True
        match.save()
        
        # Продвигаем победителя в следующий раунд
        generator = GridGenerator(match.grid)
        next_match = generator.advance_winner(match)
        
        if next_match:
            messages.success(request, f'Результат сохранён. {match.winner.full_name} проходит в следующий раунд.')
        else:
            messages.success(request, 'Результат сохранён.')
        
        return redirect('grid:view', category_id=match.grid.category.id)
    
    return redirect('tournament:list')