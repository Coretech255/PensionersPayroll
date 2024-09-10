# pension/tests.py
from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import PaymentSchedule, Payroll, Deduction
from pensioners.models import Pensioner
from users.models import CustomUser
from decimal import Decimal

class PayrollModelTests(TestCase):

    def setUp(self):
        #self.user = CustomUser.objects.create(username='username', password='password123')
                # Create a test user for associating with Pensioner
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123'
        )
        # Create a test pensioner
        self.pensioner = Pensioner.objects.create(
            user=self.user,
            first_name="John", 
            last_name="Doe",
            date_of_birth="1950-01-01",
            employment_start_date="2000-01-01",
            pension_start_date="2015-01-01"
        )

    def test_create_payroll(self):
        # Create a payroll entry
        payroll = Payroll.objects.create(
            pensioner=self.pensioner,
            payroll_date=now().date(),
            basic_salary=5000.00,
            total_deductions=0.00,
            net_salary=5000.00,
            status='unpaid'
        )
        # Test if the payroll was created correctly
        self.assertEqual(payroll.pensioner, self.pensioner)
        self.assertEqual(payroll.basic_salary, 5000.00)
        self.assertEqual(payroll.net_salary, 5000.00)
        self.assertEqual(payroll.total_deductions, 0.00)
        self.assertEqual(payroll.status, 'unpaid')

    def test_add_deduction(self):
        # Create a payroll entry
        payroll = Payroll.objects.create(
            pensioner=self.pensioner,
            payroll_date=now().date(),
            basic_salary=5000.00,
            total_deductions=0.00,
            net_salary=5000.00,
            status='unpaid'
        )

        # Add a deduction
        deduction = Deduction.objects.create(
            payroll=payroll,
            description="Tax",
            amount=500.00
        )

        # Refresh payroll to reflect the deduction
        payroll.refresh_from_db()

        # Calculate the expected net salary after deduction
        expected_net_salary = Decimal(payroll.basic_salary) - Decimal(deduction.amount)

        # Test deduction and net salary calculation
        self.assertEqual(deduction.payroll, payroll)
        self.assertEqual(deduction.amount, 500.00)
        self.assertEqual(payroll.total_deductions, deduction.amount)
        self.assertEqual(payroll.net_salary, expected_net_salary)

    def test_payment_schedule(self):
        # Create a payment schedule
        payment_schedule = PaymentSchedule.objects.create(
            pensioner=self.pensioner,
            payment_date=now().date(),
            amount=2000.00,
            status='scheduled'
        )

        # Test if the payment schedule was created correctly
        self.assertEqual(payment_schedule.pensioner, self.pensioner)
        self.assertEqual(payment_schedule.amount, 2000.00)
        self.assertEqual(payment_schedule.status, 'completed')

    def test_payroll_deductions_update(self):
        # Create a payroll entry
        payroll = Payroll.objects.create(
            pensioner=self.pensioner,
            payroll_date=now().date(),
            basic_salary=5000.00,
            total_deductions=0.00,
            net_salary=5000.00,
            status='unpaid'
        )

        # Add two deductions
        deduction1 = Deduction.objects.create(
            payroll=payroll,
            description="Tax",
            amount=500.00
        )
        deduction2 = Deduction.objects.create(
            payroll=payroll,
            description="Health Insurance",
            amount=300.00
        )

        # Refresh payroll to reflect deductions
        payroll.refresh_from_db()

        # Calculate the expected total deductions and net salary
        expected_total_deductions = deduction1.amount + deduction2.amount
        expected_net_salary = Decimal(payroll.basic_salary) - Decimal(expected_total_deductions)

        # Test total deductions and net salary calculation
        self.assertEqual(payroll.total_deductions, expected_total_deductions)
        self.assertEqual(payroll.net_salary, expected_net_salary)

    def test_payment_schedule_completion(self):
        # Create a payment schedule
        payment_schedule = PaymentSchedule.objects.create(
            pensioner=self.pensioner,
            payment_date=now().date(),
            amount=2000.00,
            status='scheduled'
        )

        # Create a payroll entry
        payroll = Payroll.objects.create(
            pensioner=self.pensioner,
            payroll_date=payment_schedule.payment_date,
            basic_salary=2000.00,
            total_deductions=0.00,
            net_salary=2000.00,
            status='paid'
        )

        # Simulate payment completion
        payment_schedule.status = 'completed'
        payment_schedule.save()

        # Refresh payment schedule
        payment_schedule.refresh_from_db()

        # Test if the payment schedule was marked as completed
        self.assertEqual(payment_schedule.status, 'completed')



class SignalTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='username', password='password123')
        self.pensioner = self.create_test_pensioner()  # Adjust as necessary to create a test pensioner instance

    def create_test_pensioner(self):
        # Create a test pensioner instance. Adjust as necessary.
        return Pensioner.objects.create(first_name="Test Pensioner",
                                        date_of_birth="1999-01-01",
                                        employment_start_date="2010-01-01",
                                        pension_start_date="2023-01-01",
                                        user_id=1,)

    def test_generate_payroll_signal(self):
        # Create a PaymentSchedule that triggers the generate_payroll signal
        payment_schedule = PaymentSchedule.objects.create(
            pensioner=self.pensioner,
            amount=1000.00,
            payment_date=now().date(),
            status='scheduled'
        )

        with transaction.atomic():  # Ensure database consistency
            payment_schedule.save()
        
        # Verify that a Payroll entry was created
        payroll = Payroll.objects.get(pensioner=self.pensioner, payroll_date=payment_schedule.payment_date)
        self.assertEqual(payroll.basic_salary, 1000.00)
        self.assertEqual(payroll.net_salary, 1000.00)
        self.assertEqual(payroll.total_deductions, 0.00)
        self.assertEqual(payroll.status, 'unpaid')

        # Verify that PaymentSchedule status was updated
        payment_schedule.refresh_from_db()
        self.assertEqual(payment_schedule.status, 'completed')

    def test_update_payroll_totals_signal(self):
        # Create a PaymentSchedule and Payroll entry
        payment_schedule = PaymentSchedule.objects.create(
            pensioner=self.pensioner,
            amount=1000.00,
            payment_date=now().date(),
            status='completed'
        )
        payroll = Payroll.objects.create(
            pensioner=self.pensioner,
            payroll_date=payment_schedule.payment_date,
            basic_salary=1000.00,
            total_deductions=0.00,
            net_salary=1000.00,
            status='unpaid'
        )

        # Create a Deduction and verify that Payroll totals are updated
        Deduction.objects.create(payroll=payroll, amount=200.00)

        payroll.refresh_from_db()
        self.assertEqual(payroll.total_deductions, 200.00)
        self.assertEqual(payroll.net_salary, 800.00)

    def test_update_payment_schedule_signal(self):
        # Create a PaymentSchedule and Payroll entry
        payment_schedule = PaymentSchedule.objects.create(
            pensioner=self.pensioner,
            amount=1000.00,
            payment_date=now().date(),
            status='scheduled'
        )
        payroll = Payroll.objects.create(
            pensioner=self.pensioner,
            payroll_date=payment_schedule.payment_date,
            basic_salary=1000.00,
            total_deductions=0.00,
            net_salary=1000.00,
            status='paid'
        )

        with transaction.atomic():  # Ensure database consistency
            payroll.save()
        
        # Verify that the related PaymentSchedule status was updated
        payment_schedule.refresh_from_db()
        self.assertEqual(payment_schedule.status, 'completed')
