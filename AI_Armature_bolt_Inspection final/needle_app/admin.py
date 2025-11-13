from django.contrib import admin
from .models import Configuration

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'plc_ip',
        'classification_model',
        'number_of_camera',
        'save_mode',
        'created_at'
    )
    search_fields = ('plc_ip', 'classification_model')
    list_filter = ('save_mode', 'number_of_camera')
    ordering = ('-created_at',)

admin.site.site_header = "AI Needle Inspection Admin"
admin.site.site_title = "AI Needle Admin Portal"
admin.site.index_title = "Welcome to the AI Needle Dashboard"
