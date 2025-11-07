from django.db import models

class TournamentGrid(models.Model):
    """Модель турнирной сетки"""
    
    GRID_TYPE_CHOICES = [
        ('single_elimination', 'Олимпийская система (на выбывание)'),
        ('double_elimination', 'Двойная олимпийская система'),
        ('round_robin', 'Круговая система'),
    ]
    
    category = models.OneToOneField(
        'Category.Category', 
        on_delete=models.CASCADE, 
        related_name='grid',
        verbose_name="Категория"
    )
    
    grid_type = models.CharField(
        max_length=30, 
        choices=GRID_TYPE_CHOICES, 
        default='single_elimination',
        verbose_name="Тип сетки"
    )
    
    is_generated = models.BooleanField(default=False, verbose_name="Сетка сгенерирована")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Турнирная сетка"
        verbose_name_plural = "Турнирные сетки"
        db_table = 'tournament_grid'
    
    def __str__(self):
        return f"Сетка для {self.category}"