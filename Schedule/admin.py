from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['match_info', 'scheduled_time', 'mat_number', 'duration_minutes', 'status']
    list_filter = ['mat_number', 'is_started', 'is_finished', 'scheduled_time']
    search_fields = ['match__athlete1__last_name', 'match__athlete2__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Матч', {
            'fields': ('match',)
        }),
        ('Время и место', {
            'fields': ('scheduled_time', 'mat_number', 'duration_minutes')
        }),
        ('Статус', {
            'fields': ('is_started', 'is_finished')
        }),
        ('Технические данные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def match_info(self, obj):
        return str(obj.match)
    match_info.short_description = 'Поединок'
    
    def status(self, obj):
        if obj.is_finished:
            return '✅ Завершён'
        elif obj.is_started:
            return '▶️ Идёт'
        return '⏳ Ожидание'
    status.short_description = 'Статус'
    
    actions = ['mark_started', 'mark_finished']
    
    def mark_started(self, request, queryset):
        updated = queryset.update(is_started=True)
        self.message_user(request, f'{updated} матчей отмечены как начатые')
    mark_started.short_description = 'Отметить как начатые'
    
    def mark_finished(self, request, queryset):
        updated = queryset.update(is_finished=True, is_started=True)
        self.message_user(request, f'{updated} матчей отмечены как завершённые')
    mark_finished.short_description = 'Отметить как завершённые'