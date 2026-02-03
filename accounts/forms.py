from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator, EmailValidator
from core.models import User

class CitizenRegistrationForm(UserCreationForm):
    # Regex Validators
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )
    aadhaar_validator = RegexValidator(
        regex=r'^\d{12}$',
        message="Aadhaar number must be exactly 12 digits."
    )
    name_validator = RegexValidator(
        regex=r'^[a-zA-Z\s]+$',
        message="Name must accept only character"
    )

    # Fields
    name = forms.CharField(
        max_length=100, 
        required=True, 
        label="Full Name",
        validators=[name_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Enter full name'})
    )
    email = forms.EmailField(
        required=True, 
        label="Email Address",
        validators=[EmailValidator(message="Enter a valid email address.")],
        widget=forms.EmailInput(attrs={'placeholder': 'user@example.com'})
    )
    phone = forms.CharField(
        max_length=10, 
        required=True, 
        validators=[phone_validator],
        help_text="10-digit mobile number",
        widget=forms.TextInput(attrs={'placeholder': '9876543210', 'pattern': '\d{10}'})
    )
    aadhaar_number = forms.CharField(
        max_length=12, 
        required=True, 
        validators=[aadhaar_validator],
        label="Aadhaar Number",
        help_text="12-digit unique identification number",
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012', 'pattern': '\d{12}'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your full address'}), 
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'name', 'email', 'phone', 'aadhaar_number', 'address')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please login instead.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'citizen'
        user.first_name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.aadhaar_number = self.cleaned_data['aadhaar_number']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class UserProfileForm(forms.ModelForm):
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )
    aadhaar_validator = RegexValidator(
        regex=r'^\d{12}$',
        message="Aadhaar number must be exactly 12 digits."
    )

    phone = forms.CharField(
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number'})
    )
    aadhaar_number = forms.CharField(
        validators=[aadhaar_validator],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12-digit Aadhaar number'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'aadhaar_number', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your residential address'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'id': 'profile_picture_input'}),
        }
