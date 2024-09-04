from django.db import models
from users.models import CustomUser
from pensioners.models import Pensioner

class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}"

class Alert(models.Model):
    ALERT_TYPES = (
        ('payment_reminder', 'Payment Reminder'),
        ('pension_status_update', 'Pension Status Update'),
    )
    pensioner = models.ForeignKey(Pensioner, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    message = models.TextField()
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=(('sent', 'Sent'), ('pending', 'Pending')), default='pending')

    def __str__(self):
        return f"{self.alert_type} for {self.pensioner}"

