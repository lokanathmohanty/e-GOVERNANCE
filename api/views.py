from django.http import JsonResponse
from core.models import Service, Application, Department
from django.views.decorators.csrf import csrf_exempt

def service_list_api(request):
    services = Service.objects.filter(is_active=True)
    data = []
    for s in services:
        data.append({
            'id': s.id,
            'name': s.service_name,
            'department': s.department.department_name,
            'days': s.processing_days,
            'fee': str(s.fee_amount)
        })
    return JsonResponse({'services': data})

def application_status_api(request, app_no):
    try:
        app = Application.objects.get(application_number=app_no)
        return JsonResponse({
            'application_number': app.application_number,
            'status': app.status,
            'applied_date': app.applied_date.strftime('%Y-%m-%d'),
            'service': app.service.service_name,
            'priority': app.priority
        })
    except Application.DoesNotExist:
        return JsonResponse({'error': 'Application not found'}, status=404)

def department_stats_api(request):
    depts = Department.objects.all()
    data = []
    for d in depts:
        data.append({
            'name': d.department_name,
            'services_count': d.services.count(),
            'total_applications': Application.objects.filter(service__department=d).count()
        })
    return JsonResponse({'departments': data})
