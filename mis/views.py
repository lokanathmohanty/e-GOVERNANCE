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
        app_count=Count('application')
    ).filter(app_count__gt=0).order_by('-app_count')[:10]
    
    # Pass as raw Python lists (json_script will handle encoding)
    service_labels = [s.service_name for s in service_stats]
    service_data = [s.app_count for s in service_stats]
    
    # Monthly Trends (Last 6 months)
    monthly_labels = []
    monthly_data = []
    for i in range(5, -1, -1):
        month_start = (timezone.now() - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        count = Application.objects.filter(
            applied_date__gte=month_start,
            applied_date__lte=month_end
        ).count()
        monthly_labels.append(month_start.strftime('%b %Y'))
        monthly_data.append(count)
    
    # SLA Compliance
    sla_on_time = 0
    sla_near_deadline = 0
    sla_delayed = delayed_apps
    
    for app in Application.objects.exclude(status__in=['approved', 'rejected']):
        time_diff = app.sla_deadline - now
        days_remaining = time_diff.days
        total_sla_days = app.service.processing_days
        
        if days_remaining < 0:
            continue  # Already counted in delayed
        elif days_remaining <= (total_sla_days * 0.2):
            sla_near_deadline += 1
        else:
            sla_on_time += 1
    
    sla_data = [sla_on_time, sla_near_deadline, sla_delayed]
    
    # Officer Performance
    officers = User.objects.filter(role='officer')
    officer_stats = []
    
    for officer in officers:
        assignments = OfficerAssignment.objects.filter(officer=officer)
        assigned_count = assignments.count()
        completed_count = assignments.filter(application__status__in=['approved', 'rejected']).count()
        pending_count = assigned_count - completed_count
        
        # Calculate average processing time
        completed_apps = Application.objects.filter(
            officer_assignments__officer=officer,
            status__in=['approved', 'rejected'],
            approved_date__isnull=False
        )
        
        avg_days = 0.0
        if completed_apps.exists():
            total_days = 0
            count = 0
            for app in completed_apps:
                if app.approved_date and app.applied_date:
                    delta = app.approved_date - app.applied_date
                    total_days += max(0, delta.days)
                    count += 1
            if count > 0:
                avg_days = round(total_days / count, 1)
        
        officer_stats.append({
            'name': officer.get_full_name() or officer.username,
            'assigned': assigned_count,
            'completed': completed_count,
            'pending': pending_count,
            'avg_days': avg_days
        })
    
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
        'officer_stats': officer_stats,
    }
    
    return render(request, 'mis/dashboard_bootstrap.html', context)

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
