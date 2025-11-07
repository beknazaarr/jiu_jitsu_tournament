from django.contrib import admin
from .models import Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'location', 'registration_open', 'is_active', 'created_at']
    list_filter = ['date', 'registration_open', 'is_active']
    search_fields = ['name', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'date', 'location', 'description', 'rules')
        }),
        ('Настройки', {
            'fields': ('registration_open', 'is_active')
        }),
        ('Технические данные', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если это новый объект
            obj.created_by = request.user
        super().save_model(request, obj, form, change)