from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import TournamentGrid


@admin.register(TournamentGrid)
class TournamentGridAdmin(admin.ModelAdmin):
    list_display = ['category', 'grid_type', 'is_generated', 'matches_count', 'view_grid_link']
    list_filter = ['grid_type', 'is_generated', 'category__tournament']
    search_fields = ['category__name', 'category__tournament__name']
    readonly_fields = ['created_at', 'matches_count']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'grid_type')
        }),
        ('Статус', {
            'fields': ('is_generated', 'matches_count')
        }),
        ('Технические данные', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def matches_count(self, obj):
        return obj.matches.count()
    matches_count.short_description = 'Количество матчей'
    
    def view_grid_link(self, obj):
        url = reverse('grid:view', args=[obj.category.id])
        return format_html('<a href="{}" target="_blank">Посмотреть сетку</a>', url)
    view_grid_link.short_description = 'Действия'