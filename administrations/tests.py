# tests.py
from django.test import TestCase
from .models import PensionScheme, Benefit
from decimal import Decimal

class PensionSchemeTest(TestCase):
    def setUp(self):
        # Create a PensionScheme instance for testing
        self.pension_scheme = PensionScheme.objects.create(
            name="Test Scheme",
            description="A scheme for testing purposes",
            eligibility_criteria="Must be 60 years or older",
            contribution_rate=Decimal('5.00')
        )

    def test_pension_scheme_str(self):
        # Test the __str__ method of PensionScheme
        self.assertEqual(str(self.pension_scheme), "Test Scheme")

class BenefitTest(TestCase):
    def setUp(self):
        # Create a PensionScheme instance
        self.pension_scheme = PensionScheme.objects.create(
            name="Test Scheme",
            description="A scheme for testing purposes",
            eligibility_criteria="Must be 60 years or older",
            contribution_rate=Decimal('5.00')
        )
        # Create a Benefit instance related to the PensionScheme
        self.benefit = Benefit.objects.create(
            pension_scheme=self.pension_scheme,
            name="Test Benefit",
            description="A benefit for testing purposes",
            value=Decimal('1000.00')
        )

    def test_benefit_str(self):
        # Test the __str__ method of Benefit
        expected_str = f"Test Benefit - {self.pension_scheme.name}"
        self.assertEqual(str(self.benefit), expected_str)

    def test_benefit_relationship(self):
        # Test the relationship between Benefit and PensionScheme
        self.assertEqual(self.benefit.pension_scheme, self.pension_scheme)
        self.assertIn(self.benefit, self.pension_scheme.benefits.all())
