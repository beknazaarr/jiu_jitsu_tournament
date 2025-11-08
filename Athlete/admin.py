from django.contrib import admin
from .models import Athlete


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'tournament', 'category', 'age', 'weight', 'school', 'is_active']
    list_filter = ['tournament', 'category', 'gender', 'is_active']
    search_fields = ['first_name', 'last_name', 'school', 'email']
    readonly_fields = ['registered_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Личные данные', {
            'fields': ('first_name', 'last_name', 'middle_name', 'birth_year', 'gender')
        }),
        ('Спортивные данные', {
            'fields': ('tournament', 'category', 'school', 'weight')
        }),
        ('Контакты', {
            'fields': ('email', 'phone')
        }),
        ('Статус', {
            'fields': ('is_active', 'registered_at')
        }),
    )
    
    actions = ['activate_athletes', 'deactivate_athletes']
    
    def activate_athletes(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано {updated} спортсменов')
    activate_athletes.short_description = 'Активировать выбранных спортсменов'
    
    def deactivate_athletes(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано {updated} спортсменов')
    deactivate_athletes.short_description = 'Деактивировать выбранных спортсменов'