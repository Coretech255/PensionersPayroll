from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile

class CustomUserModelTest(TestCase):

    def setUp(self):
        # Set up a CustomUser instance
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123',
            role='pensioner'
        )

    def test_user_creation(self):
        """Test if a CustomUser is created correctly."""
        user = get_user_model().objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'pensioner')
        self.assertTrue(user.check_password('testpassword123'))

    def test_customuser_str(self):
        """Test the __str__ method of the CustomUser model."""
        self.assertEqual(str(self.user), 'testuser (pensioner)')

class ProfileModelTest(TestCase):

    def setUp(self):
        # Set up a CustomUser instance and related Profile instance
        self.user = get_user_model().objects.create_user(
            username='profileuser',
            password='profilepassword123',
            role='payroll_officer'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            phone_number='1234567890',
            address='123 Test St',
            date_of_birth='1990-01-01',
        )

    def test_profile_creation(self):
        """Test if a Profile is created correctly and linked to the CustomUser."""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.phone_number, '1234567890')
        self.assertEqual(profile.address, '123 Test St')
        self.assertEqual(profile.date_of_birth.strftime('%Y-%m-%d'), '1990-01-01')
        self.assertEqual(profile.user.username, 'profileuser')

    def test_profile_str(self):
        """Test the __str__ method of the Profile model."""
        self.assertEqual(str(self.profile), 'Profile of profileuser')
