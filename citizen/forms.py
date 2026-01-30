from django import forms
from core.models import Application, Document, GrievanceTicket

class ServiceApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['priority', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional remarks about your application...'}),
        }

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file_path']
        widgets = {
            'document_type': forms.TextInput(attrs={'placeholder': 'e.g. ID Proof, Birth Report'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['document_type'].required = False
        self.fields['file_path'].required = False

    def clean_file_path(self):
        file = self.cleaned_data.get('file_path')
        if file:
            # Check Extension
            ext = file.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png']:
                raise forms.ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
            
            # Check Size (5MB limit)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5MB.")
        return file

class GrievanceForm(forms.ModelForm):
    class Meta:
        model = GrievanceTicket
        fields = ['application', 'subject', 'category', 'description', 'priority', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
