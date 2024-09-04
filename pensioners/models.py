from django.db import models
from users.models import CustomUser
from administrations.models import PensionScheme

def generate_pension_id():
        # Example: Generate a custom pension ID
        import uuid
        return f"P-{uuid.uuid4().hex[:6].upper()}"

class PensionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    pension_scheme = models.ForeignKey(PensionScheme, on_delete=models.CASCADE, related_name='pension_plans', null=True, blank=True)
    contribution_rate = models.DecimalField(max_digits=5, decimal_places=2)
    retirement_age = models.IntegerField()

    def __str__(self):
        return self.name

class Pensioner(models.Model):
    STATUS_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('None', 'None'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    pension_id = models.CharField(max_length=20, unique=True, default=generate_pension_id, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=STATUS_CHOICES, default='None')
    date_of_birth = models.DateField()
    pension_plan = models.ForeignKey(PensionPlan, on_delete=models.CASCADE, related_name='pensioners', null=True, blank=True)
    employment_start_date = models.DateField()
    employment_end_date = models.DateField(blank=True, null=True)
    pension_start_date = models.DateField()
    bank_name = models.CharField(max_length=100)
    bank_account_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pension_id:
            self.pension_id = generate_pension_id()
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.pension_id}"
    


class EmploymentHistory(models.Model):
    pensioner = models.ForeignKey(Pensioner, on_delete=models.CASCADE, related_name='employment_histories')
    employer_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.position} at {self.employer_name}"



