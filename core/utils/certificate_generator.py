from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse

def generate_certificate_view(request, application):
    """
    Returns a print-friendly HTML certificate for approved applications.
    """
    context = {
        'app': application,
        'citizen': application.user,
        'service': application.service,
        'dept': application.service.department,
    }
    return render(request, 'citizen/certificate.html', context)
