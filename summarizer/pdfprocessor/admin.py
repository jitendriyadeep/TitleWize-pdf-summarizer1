from django.contrib import admin
from .models import PDFDocument
from .models import UserDocumentHistory

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'summary_length')
    list_filter = ('summary_length', 'uploaded_at')
    search_fields = ('title', 'extracted_text', 'summary')
    readonly_fields = ('uploaded_at',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'file', 'summary_length')
        }),
        ('Extracted Content', {
            'fields': ('extracted_text', 'summary'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
@admin.register(UserDocumentHistory)
class UserDocumentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'document', 'action', 'accessed_at')
    list_filter = ('action', 'accessed_at')
    search_fields = ('user__username', 'document__title')
    date_hierarchy = 'accessed_at'