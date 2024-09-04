from django.db import models
from pensioners.models import Pensioner

class Payroll(models.Model):
    STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    )

    pensioner = models.ForeignKey(Pensioner, on_delete=models.CASCADE)
    payroll_date = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')

    def __str__(self):
        return f"Payroll for {self.pensioner} on {self.payroll_date}"

class Deduction(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='deductions')
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.amount}"

class PaymentSchedule(models.Model):
    pensioner = models.ForeignKey(Pensioner, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=(('scheduled', 'Scheduled'), ('completed', 'Completed')), default='scheduled')

    def __str__(self):
        return f"Payment scheduled for {self.pensioner} on {self.payment_date}"

