from django.test import TestCase, Client
from django.urls import reverse
from core.models import User, AuditLog

class CitizenRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.valid_payload = {
            'username': 'unique_citizen_123',
            'name': 'Test Citizen',
            'email': 'testcitizen@example.com',
            'phone': '9876543210',
            'aadhaar_number': '123412341234',
            'address': '123 Test St, Bhubaneswar, Odisha',
            'item': 'foobar', # Garbage to ensure strictness isn't breaking things
        }
        # Password handling in UserCreationForm is a bit special in tests if not explicit, 
        # but UserCreationForm expects password validation. 
        # We need to simulate the form fields exactly. UserCreationForm usually requires two password fields.
        # Let's check the form fields again. inheriting UserCreationForm usually implies 'password1' and 'password12'.
        # Wait, the code in forms.py says `class Meta(UserCreationForm.Meta): fields = ('username', ...)` 
        # but `UserCreationForm` itself adds `password` fields. 
        
        self.valid_payload.update({
            'password_match_check': 'TestPass@123', # Actually UserCreationForm uses 'password' or specific fields
        })
        
        # NOTE: Django's generic UserCreationForm expects 'password_1' and 'password_2' normally.
        # BUT in this environment, we verified it expects 'password1' and 'password2'.
        self.valid_payload['password1'] = 'TestPass@123'
        self.valid_payload['password2'] = 'TestPass@123'

    def test_registration_page_loads(self):
        """Test that the registration page loads successfully."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_successful_registration(self):
        """Test that a valid form submission creates a user and redirects."""
        response = self.client.post(self.register_url, self.valid_payload)
        
        # Check redirection with explicit error message if it fails
        if response.status_code != 302 and 'form' in response.context:
            self.fail(f"Registration failed with form errors: {response.context['form'].errors}")
        
        # Check redirection manually to avoid Python 3.14/Django test client compatibility issue
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('citizen:dashboard'))
        
        # Check Database
        self.assertTrue(User.objects.filter(username='unique_citizen_123').exists())
        user = User.objects.get(username='unique_citizen_123')
        self.assertEqual(user.role, 'citizen')
        self.assertEqual(user.first_name, 'Test Citizen')
        self.assertEqual(user.phone, '9876543210')
        
        # Check Audit Log
        self.assertTrue(AuditLog.objects.filter(action='REGISTER', user=user).exists())

    def test_duplicate_email_validation(self):
        """Test that registering with an existing email fails."""
        # Create user first
        User.objects.create_user(username='existing', email='testcitizen@example.com', role='citizen')
        
        response = self.client.post(self.register_url, self.valid_payload)
        
        self.assertEqual(response.status_code, 200) # Should verify failure (stay on page)
        self.assertFormError(response, 'form', 'email', "This email is already registered. Please login instead.")

    def test_invalid_phone_validation(self):
        """Test that bad phone number fails."""
        payload = self.valid_payload.copy()
        payload['phone'] = '123' # Too short
        
        response = self.client.post(self.register_url, payload)
        self.assertFormError(response, 'form', 'phone', "Phone number must be exactly 10 digits.")

    def test_invalid_aadhaar_validation(self):
        """Test that bad aadhaar number fails."""
        payload = self.valid_payload.copy()
        payload['aadhaar_number'] = 'abc' # Not digits
        
        response = self.client.post(self.register_url, payload)
        # The form regex validator message might be generic or specific. 
        # Code says: "Aadhaar number must be exactly 12 digits."
        self.assertFormError(response, 'form', 'aadhaar_number', "Aadhaar number must be exactly 12 digits.")

