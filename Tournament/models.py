from django.db import models
from django.contrib.auth.models import User

class Tournament(models.Model):
    """Модель турнира"""
    
    name = models.CharField(max_length=200, verbose_name="Название турнира")
    date = models.DateField(verbose_name="Дата проведения")
    location = models.CharField(max_length=300, verbose_name="Место проведения")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    rules = models.TextField(blank=True, null=True, verbose_name="Правила")
    
    # Настройки турнира
    registration_open = models.BooleanField(default=False, verbose_name="Регистрация открыта")
    is_active = models.BooleanField(default=True, verbose_name="Турнир активен")
    
    # Технические поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_tournaments',
        verbose_name="Создатель"
    )
    
    class Meta:
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.name} ({self.date})"