from django.db import models

class PensionScheme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    eligibility_criteria = models.TextField()
    contribution_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Benefit(models.Model):
    pension_scheme = models.ForeignKey(PensionScheme, on_delete=models.CASCADE, related_name='benefits')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.pension_scheme.name}"
