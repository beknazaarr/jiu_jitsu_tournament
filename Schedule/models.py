from django.db import models

class Schedule(models.Model):
    """Модель расписания"""
    
    match = models.OneToOneField(
        'Match.Match', 
        on_delete=models.CASCADE, 
        related_name='schedule',
        verbose_name="Поединок"
    )
    
    # Время и место
    scheduled_time = models.DateTimeField(verbose_name="Время начала")
    mat_number = models.IntegerField(verbose_name="Номер мата")
    duration_minutes = models.IntegerField(default=5, verbose_name="Продолжительность (мин)")
    
    # Статус
    is_started = models.BooleanField(default=False, verbose_name="Начался")
    is_finished = models.BooleanField(default=False, verbose_name="Завершён")
    
    # Технические поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        ordering = ['scheduled_time', 'mat_number']
        db_table = 'schedule'
    
    def __str__(self):
        return f"Мат {self.mat_number} - {self.scheduled_time.strftime('%H:%M')}"