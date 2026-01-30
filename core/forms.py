from django import forms
from .models import ContactMessage, Department

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'department', 'subject', 'message', 'attachment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'block w-full rounded-xl border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 px-4 py-3 text-sm font-medium text-gray-900 dark:text-white transition-all outline-none focus:ring-4 focus:ring-primary/10'}),
            'email': forms.EmailInput(attrs={'placeholder': 'name@example.com', 'class': 'block w-full rounded-xl border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 px-4 py-3 text-sm font-medium text-gray-900 dark:text-white transition-all outline-none focus:ring-4 focus:ring-primary/10'}),
            'department': forms.Select(attrs={'class': 'block w-full rounded-xl border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 px-4 py-3 text-sm font-medium text-gray-900 dark:text-white transition-all outline-none focus:ring-4 focus:ring-primary/10 appearance-none'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Brief summary of your inquiry', 'class': 'block w-full rounded-xl border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 px-4 py-3 text-sm font-medium text-gray-900 dark:text-white transition-all outline-none focus:ring-4 focus:ring-primary/10'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Please describe your issue or inquiry in detail...', 'class': 'block w-full rounded-xl border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 px-4 py-3 text-sm font-medium text-gray-900 dark:text-white transition-all outline-none focus:ring-4 focus:ring-primary/10'}),
            'attachment': forms.FileInput(attrs={'class': 'hidden', 'id': 'file-upload'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].empty_label = "General Inquiry"
        self.fields['department'].required = False
