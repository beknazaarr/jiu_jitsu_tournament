import random
import math
from Match.models import Match


class GridGenerator:
    """Генератор турнирных сеток"""
    
    ROUND_NAMES = {
        1: 'final',
        2: 'semifinal',
        4: 'quarterfinal',
        8: 'round_of_16',
        16: 'round_of_32',
    }
    
    def __init__(self, grid):
        self.grid = grid
        self.category = grid.category
        
    def generate_single_elimination(self):
        """Генерация олимпийской системы (на выбывание)"""
        # Получаем всех активных спортсменов категории
        athletes = list(
            self.category.athletes.filter(is_active=True).order_by('?')
        )
        
        if len(athletes) < 2:
            raise ValueError("Недостаточно участников для создания сетки (минимум 2)")
        
        # Определяем количество раундов
        num_athletes = len(athletes)
        num_rounds = math.ceil(math.log2(num_athletes))
        total_positions = 2 ** num_rounds
        
        # Удаляем старые матчи, если они есть
        self.grid.matches.all().delete()
        
        # Создаём первый раунд
        first_round_matches = total_positions // 2
        match_number = 1
        
        # Определяем название первого раунда
        first_round_name = self.ROUND_NAMES.get(first_round_matches, 'preliminary')
        
        # Создаём пары для первого раунда
        for i in range(first_round_matches):
            athlete1 = athletes[i] if i < len(athletes) else None
            athlete2 = athletes[i + first_round_matches] if (i + first_round_matches) < len(athletes) else None
            
            if athlete1:  # Создаём матч только если есть хотя бы один участник
                Match.objects.create(
                    grid=self.grid,
                    athlete1=athlete1,
                    athlete2=athlete2,
                    round=first_round_name,
                    match_number=match_number
                )
                match_number += 1
        
        # Создаём заглушки для следующих раундов
        current_matches = first_round_matches
        current_round = num_rounds - 1
        
        while current_matches > 1:
            current_matches //= 2
            round_name = self.ROUND_NAMES.get(current_matches, 'preliminary')
            
            for i in range(current_matches):
                Match.objects.create(
                    grid=self.grid,
                    athlete1=None,  # Будет заполнено после завершения предыдущих матчей
                    athlete2=None,
                    round=round_name,
                    match_number=match_number
                )
                match_number += 1
            
            current_round -= 1
        
        # Помечаем сетку как сгенерированную
        self.grid.is_generated = True
        self.grid.save()
        
        return self.grid.matches.count()
    
    def advance_winner(self, match):
        """Продвигает победителя в следующий раунд"""
        if not match.winner or not match.is_completed:
            return None
        
        # Определяем, в какой матч следующего раунда попадает победитель
        current_round_matches = Match.objects.filter(
            grid=self.grid,
            round=match.round
        ).order_by('match_number')
        
        current_position = list(current_round_matches).index(match)
        next_position = current_position // 2
        
        # Находим следующий раунд
        round_order = ['round_of_32', 'round_of_16', 'quarterfinal', 'semifinal', 'final']
        try:
            current_index = round_order.index(match.round)
            if current_index < len(round_order) - 1:
                next_round = round_order[current_index + 1]
                
                # Находим матч следующего раунда
                next_matches = Match.objects.filter(
                    grid=self.grid,
                    round=next_round
                ).order_by('match_number')
                
                if next_position < len(next_matches):
                    next_match = next_matches[next_position]
                    
                    # Добавляем победителя в следующий матч
                    if not next_match.athlete1:
                        next_match.athlete1 = match.winner
                    else:
                        next_match.athlete2 = match.winner
                    
                    next_match.save()
                    return next_match
        except (ValueError, IndexError):
            pass
        
        return None
    
    def get_bracket_structure(self):
        """Возвращает структуру сетки для отображения"""
        rounds = {}
        
        for match in self.grid.matches.all().order_by('match_number'):
            if match.round not in rounds:
                rounds[match.round] = []
            rounds[match.round].append(match)
        
        # Сортируем раунды в правильном порядке
        round_order = ['round_of_32', 'round_of_16', 'quarterfinal', 'semifinal', 'final']
        sorted_rounds = []
        
        for round_name in round_order:
            if round_name in rounds:
                sorted_rounds.append({
                    'name': round_name,
                    'display_name': dict(Match.ROUND_CHOICES).get(round_name, round_name),
                    'matches': rounds[round_name]
                })
        
        return sorted_rounds