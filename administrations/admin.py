from django.contrib import admin
from .models import PensionScheme, Benefit

class BenefitInline(admin.TabularInline):
    model = Benefit
    extra = 1

class PensionSchemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'contribution_rate', 'created_on')
    inlines = [BenefitInline]

admin.site.register(PensionScheme, PensionSchemeAdmin)

