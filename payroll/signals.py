# pension/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import PaymentSchedule, Payroll, Deduction
from django.db.models import Sum

@receiver(post_save, sender=PaymentSchedule)
def generate_payroll(sender, instance, **kwargs):
    # Ensure that payroll is created only if the schedule is not yet completed
    if instance.status == 'scheduled' and instance.payment_date <= now().date():
        # Create a Payroll entry
        # Example: Basic salary and net salary are the same for simplicity
        payroll = Payroll.objects.create(
            pensioner=instance.pensioner,
            payroll_date=instance.payment_date,
            basic_salary=instance.amount,  # Assuming amount is the basic salary
            total_deductions=0.00,  # Set default deduction to 0.00 or calculate as needed
            net_salary=instance.amount,  # Net salary assumed same as basic salary for simplicity
            status='unpaid'
        )
        # Update PaymentSchedule status
        instance.status = 'completed'
        instance.save()

        # Recalculate total_deductions and net_salary
        update_payroll_totals(payroll)

@receiver(post_save, sender=Deduction)
def update_payroll_totals(sender, instance, **kwargs):
    # Get the related Payroll instance
    payroll = instance.payroll
    # Calculate total deductions for the related Payroll
    total_deductions = Deduction.objects.filter(payroll=payroll).aggregate(total=Sum('amount'))['total'] or 0
    payroll.total_deductions = total_deductions
    payroll.net_salary = payroll.basic_salary - total_deductions
    payroll.save()

@receiver(post_save, sender=Payroll)
def update_payment_schedule(sender, instance, **kwargs):
    if instance.status == 'paid':
        # Find related PaymentSchedules for the same date and pensioner
        schedules = PaymentSchedule.objects.filter(pensioner=instance.pensioner, payment_date=instance.payroll_date)
        for schedule in schedules:
            if schedule.status == 'scheduled':
                schedule.status = 'completed'
                schedule.save()
