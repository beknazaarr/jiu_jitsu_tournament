from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'tournament', 'gender', 'age_range', 'weight_range', 'level', 'athletes_count']
    list_filter = ['tournament', 'gender', 'level']
    search_fields = ['name', 'tournament__name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('tournament', 'name', 'level')
        }),
        ('Параметры категории', {
            'fields': ('gender', 'age_min', 'age_max', 'weight_min', 'weight_max')
        }),
        ('Технические данные', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def age_range(self, obj):
        return f"{obj.age_min}-{obj.age_max} лет"
    age_range.short_description = 'Возраст'
    
    def weight_range(self, obj):
        return f"{obj.weight_min}-{obj.weight_max} кг"
    weight_range.short_description = 'Вес'
    
    def athletes_count(self, obj):
        return obj.athletes.filter(is_active=True).count()
    athletes_count.short_description = 'Участников'