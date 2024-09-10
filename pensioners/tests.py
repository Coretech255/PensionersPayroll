from django.test import TestCase
from users.models import CustomUser
from administrations.models import PensionScheme
from .models import PensionPlan, Pensioner, EmploymentHistory

class PensionPlanModelTest(TestCase):

    def setUp(self):
        self.pension_scheme = PensionScheme.objects.create(name="Government Scheme", contribution_rate=5.5)
        self.pension_plan = PensionPlan.objects.create(
            name="Basic Pension Plan",
            description="A simple pension plan for all employees",
            pension_scheme=self.pension_scheme,
            contribution_rate=5.5,
            retirement_age=60
        )

    def test_pension_plan_creation(self):
        """Test if a PensionPlan is created correctly."""
        pension_plan = PensionPlan.objects.get(name="Basic Pension Plan")
        self.assertEqual(pension_plan.name, "Basic Pension Plan")
        self.assertEqual(pension_plan.description, "A simple pension plan for all employees")
        self.assertEqual(pension_plan.contribution_rate, 5.5)
        self.assertEqual(pension_plan.retirement_age, 60)

    def test_pension_plan_str(self):
        """Test the __str__ method of PensionPlan."""
        self.assertEqual(str(self.pension_plan), "Basic Pension Plan")


class PensionerModelTest(TestCase):

    def setUp(self):
        # Create a CustomUser instance
        self.user = CustomUser.objects.create_user(username='testuser', password='password123')
        
        # Create a PensionPlan instance
        self.pension_scheme = PensionScheme.objects.create(name="Government Scheme", contribution_rate=5.5)
