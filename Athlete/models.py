from django.db import models

class Athlete(models.Model):
    """Модель спортсмена"""
    
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    # Личные данные
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    birth_year = models.IntegerField(verbose_name="Год рождения")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    
    # Спортивные данные
    school = models.CharField(max_length=200, verbose_name="Школа/Зал")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Вес (кг)")
    
    # Контактная информация
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    
    # Связь с турниром и категорией
    tournament = models.ForeignKey(
        'Tournament.Tournament', 
        on_delete=models.CASCADE, 
        related_name='athletes',
        verbose_name="Турнир"
    )
    category = models.ForeignKey(
        'Category.Category', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='athletes',
        verbose_name="Категория"
    )
    
    # Технические поля
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    class Meta:
        verbose_name = "Спортсмен"
        verbose_name_plural = "Спортсмены"
        ordering = ['last_name', 'first_name']
        db_table = 'athlete'
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"
    
    @property
    def age(self):
        from datetime import datetime
        return datetime.now().year - self.birth_year