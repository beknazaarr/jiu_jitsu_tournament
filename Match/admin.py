from django.contrib import admin
from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['match_number', 'grid', 'round_display', 'match_description', 'winner', 'is_completed']
    list_filter = ['grid__category__tournament', 'round', 'is_completed']
    search_fields = ['athlete1__last_name', 'athlete2__last_name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_completed']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('grid', 'round', 'match_number')
        }),
        ('Участники', {
            'fields': ('athlete1', 'athlete2')
        }),
        ('Результаты', {
            'fields': ('winner', 'score_athlete1', 'score_athlete2', 'result_type', 'is_completed')
        }),
        ('Технические данные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def round_display(self, obj):
        return dict(Match.ROUND_CHOICES).get(obj.round, obj.round)
    round_display.short_description = 'Раунд'
    
    def match_description(self, obj):
        if obj.athlete2:
            return f"{obj.athlete1.last_name} vs {obj.athlete2.last_name}"
        return f"{obj.athlete1.last_name} vs TBD"
    match_description.short_description = 'Поединок'
    
    actions = ['mark_completed', 'mark_incomplete']
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f'Отмечено {updated} матчей как завершённые')
    mark_completed.short_description = 'Отметить как завершённые'
    
    def mark_incomplete(self, request, queryset):
        updated = queryset.update(is_completed=False)
        self.message_user(request, f'Отмечено {updated} матчей как незавершённые')
    mark_incomplete.short_description = 'Отметить как незавершённые'