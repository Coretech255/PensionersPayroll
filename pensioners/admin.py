from django.contrib import admin
from .models import Pensioner, EmploymentHistory, PensionPlan

class EmploymentHistoryInline(admin.TabularInline):
    model = EmploymentHistory
    extra = 1

class PensionerAdmin(admin.ModelAdmin):
    list_display = ('pension_id', 'first_name', 'last_name', 'bank_name', 'pension_start_date')
    search_fields = ('pension_id', 'first_name', 'last_name', 'bank_name')
    inlines = [EmploymentHistoryInline]

admin.site.register(Pensioner, PensionerAdmin)
admin.site.register(PensionPlan)

