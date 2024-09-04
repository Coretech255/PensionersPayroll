from django.contrib import admin
from .models import Payroll, Deduction, PaymentSchedule
from django.http import HttpResponse
import csv

class DeductionInline(admin.TabularInline):
    model = Deduction
    extra = 1

class PayrollAdmin(admin.ModelAdmin):
    list_display = ('pensioner', 'payroll_date', 'net_salary', 'status')
    list_filter = ('status', 'payroll_date')
    inlines = [DeductionInline]

    def export_as_csv(self, request, queryset):
        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="payroll_report.csv"'
        writer = csv.writer(response)
        
        # Write the headers
        writer.writerow(['Pensioner', 'Payroll Date', 'Net Salary', 'Status'])
        
        # Write the data rows
        for payroll in queryset:
            writer.writerow([payroll.pensioner, payroll.payroll_date, payroll.net_salary, payroll.status])
        
        return response
    
    export_as_csv.short_description = "Export Selected as CSV"
    
    actions = [export_as_csv]

admin.site.register(Payroll, PayrollAdmin)
admin.site.register(PaymentSchedule)


