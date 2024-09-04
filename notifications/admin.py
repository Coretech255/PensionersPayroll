from django.contrib import admin
from .models import Notification, Alert

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'created_at', 'read_status')
    list_filter = ('read_status', 'created_at')

class AlertAdmin(admin.ModelAdmin):
    list_display = ('pensioner', 'alert_type', 'scheduled_time', 'status')
    list_filter = ('alert_type', 'status', 'scheduled_time')

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Alert, AlertAdmin)
