from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Department, Service, User, Application
from django.contrib import messages

from functools import wraps

def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied.")
        return redirect('core:home')
    return wrapper

@login_required
@admin_only
def dashboard(request):
    from core.models import SystemConfiguration, AuditLog, GrievanceTicket
    from django.db.models import Count, Avg, F
    from django.utils import timezone
    from datetime import timedelta

    # Ensure config exists
    config, _ = SystemConfiguration.objects.get_or_create(id=1)
    
    dept_count = Department.objects.count()
    service_count = Service.objects.count()
    user_count = User.objects.count()
    total_apps = Application.objects.count()
    unassigned_apps = Application.objects.filter(officer_assignments__isnull=True).count()
    
    # User Management & Access Metrics
    recent_users = User.objects.order_by('-date_joined')[:5]
    inactive_users = User.objects.filter(last_login__lt=timezone.now() - timedelta(days=30)).count()
    officer_count = User.objects.filter(role='officer').count()
    
    # Application & Performance Metrics
    recent_apps = Application.objects.select_related('user', 'service').order_by('-applied_date')[:5]
    approved_apps = Application.objects.filter(status='approved').count()
    rejected_apps = Application.objects.filter(status='rejected').count()
    app_surge = Application.objects.filter(applied_date__gte=timezone.now() - timedelta(days=1)).count() > 50
    
    # Audit & Security Metrics
    failed_logins = AuditLog.objects.filter(action='LOGIN', description__icontains='fail').count()
    recent_logs = AuditLog.objects.order_by('-timestamp')[:10]
    
    # System Health (Mock / Simple checks)
    health_status = {
        'cpu': 15, 'memory': 32, 'uptime': '99.99%', 'api_latency': '45ms',
        'database': 'Healthy', 'storage': '14%'
    }
    
    # Service Analytics
    top_services = Service.objects.annotate(num_apps=Count('application_set')).order_by('-num_apps')[:3]
    
    # Department Performance & Onboarding Metrics
    dept_performance = Department.objects.annotate(
        avg_processing=Avg('services__processing_days'),
        total_load=Count('services__application_set')
    ).order_by('-total_load')[:5]
    
    onboarding_completion = {
        'total': user_count,
        'completed': User.objects.filter(is_active=True).count(),
        'pending_verification': User.objects.filter(is_verified=False).count() if hasattr(User, 'is_verified') else 0
    }
    
    context = {
        'config': config,
        'dept_count': dept_count,
        'service_count': service_count,
        'user_count': user_count,
        'officer_count': officer_count,
        'inactive_users': inactive_users,
        'total_apps': total_apps,
        'unassigned_apps': unassigned_apps,
        'approved_apps': approved_apps,
        'rejected_apps': rejected_apps,
        'app_surge': app_surge,
        'recent_users': recent_users,
        'recent_apps': recent_apps,
        'recent_logs': recent_logs,
        'health': health_status,
        'top_services': top_services,
        'failed_logins': failed_logins,
        'dept_performance': dept_performance,
        'onboarding': onboarding_completion,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@admin_only
def manage_departments(request):
    depts = Department.objects.all()
    return render(request, 'admin_panel/departments.html', {'departments': depts})

@login_required
@admin_only
def manage_services(request):
    services = Service.objects.all()
    return render(request, 'admin_panel/services.html', {'services': services})

@login_required
@admin_only
def view_audit_logs(request):
    from core.models import AuditLog
    logs = AuditLog.objects.all().order_by('-timestamp')[:100]
    return render(request, 'admin_panel/audit_logs.html', {'logs': logs})

@login_required
@admin_only
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})

@login_required
@admin_only
def manage_announcements(request):
    from core.models import Announcement
    
    if request.method == 'POST':
        # Simple processing for creation/deletion could be handled here or separate views
        # For quickly testing, let's assume this is just the list view
        pass
        
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/announcements.html', {'announcements': announcements})

@login_required
@admin_only
def create_announcement(request):
    from core.models import Announcement
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        priority = request.POST.get('priority')
        image = request.FILES.get('image')
        document = request.FILES.get('document')
        
        Announcement.objects.create(
            title=title, 
            content=content, 
            category=category, 
            priority=priority,
            image=image,
            document=document
        )
        messages.success(request, "Announcement published.")
        return redirect('admin_panel:announcements')
        
    return render(request, 'admin_panel/announcement_form.html')
