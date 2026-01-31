from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .forms import ContactForm
from .models import Notification

def home(request):
    from core.models import Department
    import json
    departments = Department.objects.filter(is_active=True)

    # Serialize for Map
    dept_list = []
    for dept in departments:
        if dept.latitude and dept.longitude:
            try:
                dept_list.append({
                    'name': dept.department_name,
                    'lat': float(dept.latitude),
                    'lng': float(dept.longitude)
                })
            except (ValueError, TypeError):
                continue
    
    # Pass list directly for json_script
    # departments_json = json.dumps(dept_list)
    
    # Live Stats
    try:
        from core.models import Application
        total_apps = Application.objects.count()
        issued_certs = Application.objects.filter(status='approved').count()
    except:
        total_apps = 12500
        issued_certs = 9800
        
    stats = {
        'total': total_apps,
        'issued': issued_certs,
        'satisfaction': 98,
        'time': 3
    }
    
    # Announcements & Notices
    from core.models import Announcement
    from django.utils import timezone
    now = timezone.now()
    
    # Alerts (For Ticker and Emergency Bar)
    alerts = Announcement.objects.filter(category='alert', is_active=True).filter(Q(expires_at__isnull=True) | Q(expires_at__gte=now))
    
    # News (For Cards)
    latest_news = Announcement.objects.filter(category__in=['news', 'policy'], is_active=True).filter(Q(expires_at__isnull=True) | Q(expires_at__gte=now))[:3]
    
    # Circulars & Downloads (For Sidebar list)
    notices = Announcement.objects.filter(category__in=['circular', 'tender', 'deadline'], is_active=True).filter(Q(expires_at__isnull=True) | Q(expires_at__gte=now))[:5]
    
    context = {
        'departments': departments,
        'stats': stats,
        'dept_list': dept_list,
        'alerts': alerts,
        'latest_news': latest_news,
        'notices': notices
    }
    
    return render(request, 'home.html', context)

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully! We will get back to you soon.")
            return redirect('core:contact')
        else:
            messages.error(request, "There was an error in your submission. Please check the form.")
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})

@login_required
def mark_notification_read(request, notif_id):
    if request.method == 'POST':
        notif = get_object_or_404(Notification, id=notif_id, user=request.user)
        notif.is_read = True
        notif.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def mark_all_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
    
@login_required
def all_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': notifications})


def about(request):
    return render(request, 'footer/about.html')

def services_list(request):
    return render(request, 'footer/services_list.html')

def dashboard_info_view(request):
    if request.user.is_authenticated:
        return redirect('citizen:dashboard')
    return render(request, 'footer/dashboard_info.html')

def help_page(request):
    return render(request, 'footer/help.html')

def manuals(request):
    return render(request, 'footer/manuals.html')

def privacy(request):
    return render(request, 'footer/privacy.html')

def terms(request):
    return render(request, 'footer/terms.html')

def accessibility(request):
    return render(request, 'footer/accessibility.html')

def verify_public_certificate(request):
    app_id = request.GET.get('id', '').strip()
    if not app_id:
        return JsonResponse({'valid': False, 'message': 'Please provide an Application ID.'})
    
    try:
        from core.models import Application
        
        # Try finding by exact Application Number first
        app = Application.objects.filter(application_number__iexact=app_id).first()
        
        # Fallback to PK if it's numeric
        if not app and app_id.isdigit():
            app = Application.objects.filter(id=app_id).first()
            
        # Fallback to icontains for partial match
        if not app:
            app = Application.objects.filter(application_number__icontains=app_id).first()
            
        if not app:
            return JsonResponse({'valid': False, 'message': 'Certificate not found.'})
        
        if app.status == 'approved':
            username = app.user.get_full_name() or app.user.username
            # Mask the name more gracefully
            if len(username) > 3:
                masked_name = username[:2] + '*' * (len(username)-4) + username[-2:]
            else:
                masked_name = username[0] + '*' * (len(username)-1) if len(username) > 1 else username
            
            return JsonResponse({
                'valid': True,
                'applicant': masked_name,
                'service': app.service.service_name,
                'date': app.applied_date.strftime('%d %b %Y')
            })
        else:
            return JsonResponse({'valid': False, 'message': f'Application status is {app.get_status_display()}'})
            
    except Exception as e:
        return JsonResponse({'valid': False, 'message': 'An error occurred during verification.'})

from django.utils import timezone
def health_check(request):
    return JsonResponse({'status': 'ok', 'timestamp': timezone.now().isoformat()})
