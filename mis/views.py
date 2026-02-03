from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Application, Department, User, Service, OfficerAssignment
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from core.decorators import role_required

@login_required
@role_required(['department_head', 'admin'])
def dashboard(request):
    if request.user.role not in ['admin', 'department_head']:
        messages.error(request, "Access denied. MIS restricted to management.")
        return redirect('core:home')
    
    # Global Stats
    total_apps = Application.objects.count()
    approved_apps = Application.objects.filter(status='approved').count()
    rejected_apps = Application.objects.filter(status='rejected').count()
    pending_apps = Application.objects.filter(status='pending').count()
    in_progress_apps = Application.objects.filter(status='under_review').count()
    
    # SLA Delayed (Apps where deadline passed and still not completed)
    now = timezone.now()
    delayed_apps = Application.objects.filter(
        sla_deadline__lt=now
    ).exclude(status__in=['approved', 'rejected']).count()
    
    # Service-wise Distribution
    service_stats = Service.objects.annotate(
        app_count=Count('application_set')
    ).filter(app_count__gt=0).order_by('-app_count')[:10]
    
    # ... (skipping unchanged code) ...
    
    # Department-wise Stats
    dept_stats = Department.objects.annotate(
        app_count=Count('services__application_set'),
        approved_count=Count('services__application_set', filter=Q(services__application__status='approved')),
        pending_count=Count('services__application_set', filter=Q(services__application__status='pending'))
    ).filter(app_count__gt=0)
    
    stats = {
        'total': total_apps,
        'pending': pending_apps,
        'in_progress': in_progress_apps,
        'approved': approved_apps,
        'rejected': rejected_apps,
        'delayed': delayed_apps,
        'unassigned': Application.objects.filter(officer_assignments__isnull=True).count()
    }
    
    context = {
        'stats': stats,
        'service_labels': service_labels,
        'service_data': service_data,
        'monthly_labels': monthly_labels,
        'monthly_data': monthly_data,
        'sla_data': sla_data,
        'sla_compliance': sla_compliance,
        'officer_stats': officer_stats,
        'dept_stats': dept_stats,
    }
    
    return render(request, 'mis/dashboard.html', context)

@login_required
@role_required(['department_head', 'admin'])
def contact_inbox(request):
    """
    View for Dept Heads to see Contact Us messages.
    """
    from core.models import ContactMessage
    
    # Filter: Admin sees all, Dept Head sees only their dept or general (null)
    if request.user.role == 'admin':
        msgs = ContactMessage.objects.all().order_by('-created_at')
    else:
        # Get head's departments
        my_depts = request.user.headed_departments.all()
        msgs = ContactMessage.objects.filter(
            Q(department__in=my_depts) | Q(department__isnull=True)
        ).order_by('-created_at')

    context = {
        'messages_list': msgs,
        'messages': msgs, # Duplicate for count in template
        'unread_count': msgs.filter(is_resolved=False).count(),
        'resolved_count': msgs.filter(is_resolved=True).count()
    }
    return render(request, 'mis/contact_inbox.html', context)

@login_required
@role_required(['department_head', 'admin'])
def reply_contact(request, msg_id):
    """
    Handle replying to a contact message.
    """
    from core.models import ContactMessage
    from django.core.mail import send_mail
    from django.conf import settings
    
    msg = get_object_or_404(ContactMessage, id=msg_id)
    
    # Permission check (Department Head can only reply to their dept msgs)
    if request.user.role != 'admin' and msg.department:
        if not request.user.headed_departments.filter(id=msg.department.id).exists():
            messages.error(request, "You do not have permission to reply to this department's messages.")
            return redirect('mis:contact_inbox')

    if request.method == 'POST':
        reply_text = request.POST.get('reply_message')
        mark_resolved = request.POST.get('mark_resolved') == 'on'
        
        if reply_text:
            # Send Email
            try:
                subject = f"Re: {msg.subject} - eGovernance Portal Response"
                email_body = f"""Dear {msg.name},\n\n{reply_text}\n\n--\nRegards,\n{request.user.get_full_name()}\n{msg.department.department_name if msg.department else 'e-Gov Support Team'}"""
                
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL or 'noreply@egov.com',
                    [msg.email],
                    fail_silently=False,
                )
                messages.success(request, f"Reply sent to {msg.email} successfully.")
                
                if mark_resolved:
                    msg.is_resolved = True
                    msg.save()
                    
            except Exception as e:
                messages.error(request, f"Error sending email: {str(e)}")
        
    return redirect('mis:contact_inbox')
@login_required
@role_required(['department_head', 'admin'])
def service_list(request):
    from core.models import Service
    
    if request.user.role == 'admin':
        services = Service.objects.all().select_related('department')
    else:
        services = Service.objects.filter(department__in=request.user.headed_departments.all()).select_related('department')
        
    return render(request, 'mis/service_list.html', {'services': services})

@login_required
@role_required(['department_head', 'admin'])
def service_create(request):
    from .forms import ServiceForm
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully.")
            return redirect('mis:service_list')
    else:
        form = ServiceForm(user=request.user)
    
    return render(request, 'mis/service_form.html', {'form': form, 'title': 'Add New Service'})

@login_required
@role_required(['department_head', 'admin'])
def service_edit(request, service_id):
    from core.models import Service
    from .forms import ServiceForm
    
    service = get_object_or_404(Service, id=service_id)
    
    # Permission check
    if request.user.role != 'admin' and service.department not in request.user.headed_departments.all():
        messages.error(request, "You cannot edit services from other departments.")
        return redirect('mis:service_list')
        
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully.")
            return redirect('mis:service_list')
    else:
        form = ServiceForm(instance=service, user=request.user)
    
    return render(request, 'mis/service_form.html', {'form': form, 'title': 'Edit Service', 'service': service})

@login_required
@role_required(['department_head', 'admin'])
def export_reports(request):
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="application_report_{timezone.now().date()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Application ID', 'Citizen', 'Service', 'Department', 'Status', 'Applied Date', 'SLA Status', 'Completed Date'])
    
    if request.user.role == 'admin':
        apps = Application.objects.all().select_related('user', 'service', 'service__department')
    else:
        apps = Application.objects.filter(
            service__department__in=request.user.headed_departments.all()
        ).select_related('user', 'service', 'service__department')
        
    for app in apps:
        writer.writerow([
            app.application_number,
            app.user.get_full_name() or app.user.username,
            app.service.service_name,
            app.service.department.department_name,
            app.get_status_display(),
            app.applied_date.strftime('%Y-%m-%d %H:%M'),
            'On Time' if app.sla_deadline > timezone.now() else 'Delayed',
            app.approved_date.strftime('%Y-%m-%d %H:%M') if app.approved_date else '-'
        ])
        
    return response
