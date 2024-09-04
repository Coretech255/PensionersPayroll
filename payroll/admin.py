from django.contrib import admin
from .models import Payroll, Deduction, PaymentSchedule

class DeductionInline(admin.TabularInline):
    model = Deduction
    extra = 1

class PayrollAdmin(admin.ModelAdmin):
    list_display = ('pensioner', 'payroll_date', 'net_salary', 'status')
    list_filter = ('status', 'payroll_date')
    inlines = [DeductionInline]

admin.site.register(Payroll, PayrollAdmin)
admin.site.register(PaymentSchedule)

