from django.contrib import admin
from .models import PageVisit

# Register your models here.
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'page_name', 'time_spent_seconds', 'created_at')
    list_filter = ('user', 'page_name', 'created_at')
    search_fields = ('page_name',)

admin.site.register(PageVisit, PageVisitAdmin)
