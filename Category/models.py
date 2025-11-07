from django.db import models

class Category(models.Model):
    """Модель категории (возраст, вес, уровень)"""
    
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
        ('professional', 'Профессионал'),
    ]
    
    tournament = models.ForeignKey(
        'Tournament.Tournament',
        on_delete=models.CASCADE, 
        related_name='categories',
        verbose_name="Турнир"
    )
    
    name = models.CharField(max_length=200, verbose_name="Название категории")
    
    # Параметры категории
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    age_min = models.IntegerField(verbose_name="Минимальный возраст")
    age_max = models.IntegerField(verbose_name="Максимальный возраст")
    weight_min = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Минимальный вес (кг)")
    weight_max = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Максимальный вес (кг)")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name="Уровень")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['age_min', 'weight_min']
        db_table = 'category'
    
    def __str__(self):
        return f"{self.name} ({self.tournament.name})"