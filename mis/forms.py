from django import forms
from core.models import Service, Department

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'department', 'description', 'required_documents', 'processing_days', 'fee_amount', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'required_documents': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comma separated, e.g. Aadhar Card, Photo, Utility Bill'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role == 'department_head':
            self.fields['department'].queryset = user.headed_departments.all()
        
        for field in self.fields:
            if field != 'is_active':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
