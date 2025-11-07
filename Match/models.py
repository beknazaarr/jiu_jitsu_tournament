from django.db import models

class Match(models.Model):
    """Модель поединка"""
    
    ROUND_CHOICES = [
        ('final', 'Финал'),
        ('semifinal', 'Полуфинал'),
        ('quarterfinal', 'Четвертьфинал'),
        ('round_of_16', '1/8 финала'),
        ('round_of_32', '1/16 финала'),
        ('preliminary', 'Предварительный раунд'),
    ]
    
    RESULT_CHOICES = [
        ('submission', 'Сабмишн'),
        ('points', 'По очкам'),
        ('disqualification', 'Дисквалификация'),
        ('technical', 'Техническая победа'),
        ('walkover', 'Неявка соперника'),
    ]
    
    grid = models.ForeignKey(
        'TournamentGrid.TournamentGrid', 
        on_delete=models.CASCADE, 
        related_name='matches',
        verbose_name="Сетка"
    )
    
    # Участники
    athlete1 = models.ForeignKey(
        'Athlete.Athlete', 
        on_delete=models.CASCADE, 
        related_name='matches_as_athlete1',
        verbose_name="Спортсмен 1"
    )
    athlete2 = models.ForeignKey(
        'Athlete.Athlete', 
        on_delete=models.CASCADE, 
        related_name='matches_as_athlete2',
        null=True,
        blank=True,
        verbose_name="Спортсмен 2"
    )
    
    # Информация о поединке
    round = models.CharField(max_length=20, choices=ROUND_CHOICES, verbose_name="Раунд")
    match_number = models.IntegerField(verbose_name="Номер боя")
    
    # Результаты
    winner = models.ForeignKey(
        'Athlete.Athlete', 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='won_matches',
        verbose_name="Победитель"
    )
    score_athlete1 = models.IntegerField(default=0, verbose_name="Счёт спортсмена 1")
    score_athlete2 = models.IntegerField(default=0, verbose_name="Счёт спортсмена 2")
    result_type = models.CharField(
        max_length=20, 
        choices=RESULT_CHOICES, 
        blank=True,
        null=True,
        verbose_name="Способ победы"
    )
    
    # Статус
    is_completed = models.BooleanField(default=False, verbose_name="Завершён")
    
    # Технические поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Поединок"
        verbose_name_plural = "Поединки"
        ordering = ['match_number']
        db_table = 'match'
    
    def __str__(self):
        if self.athlete2:
            return f"{self.athlete1.last_name} vs {self.athlete2.last_name}"
        return f"{self.athlete1.last_name} vs TBD"