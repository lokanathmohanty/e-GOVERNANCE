from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Application, OfficerAssignment, AuditLog, Document
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
from core.decorators import role_required

@login_required
@role_required(['officer', 'admin'])
def dashboard(request):
    if request.user.role not in ['officer', 'department_head', 'admin']:
        messages.error(request, "Access denied.")
        return redirect('core:home')
    
    # Filtering logic for sidebar links
    filter_type = request.GET.get('filter', 'all')
    search_query = request.GET.get('q', '')
    
    # Get assignments for this officer
    assignments = OfficerAssignment.objects.filter(
        officer=request.user
    ).select_related(
        'application', 
        'application__service',
        'application__service__department',
        'application__user'
    ).order_by('-assigned_date')
    
    if search_query:
        assignments = assignments.filter(
            Q(application__application_number__icontains=search_query) |
            Q(application__user__username__icontains=search_query) |
            Q(application__user__email__icontains=search_query)
        )
    
    if filter_type == 'pending':
        assignments = assignments.filter(application__status='pending')
    elif filter_type == 'history':
        assignments = assignments.filter(application__status__in=['approved', 'rejected'])
    elif filter_type == 'in_progress':
        assignments = assignments.filter(application__status='under_review')
    
    # Convert to list to persist attributes added effectively
    assignments = list(assignments)
    
    # Calculate SLA status for each assignment
    now = timezone.now()
    for assignment in assignments:
        app = assignment.application
        if app.status in ['approved', 'rejected']:
            app.sla_status = 'completed'
        else:
            time_diff = app.sla_deadline - now
            days_remaining = time_diff.days
            total_sla_days = app.service.processing_days
            
            if days_remaining < 0:
                app.sla_status = 'delayed'
                app.days_overdue = abs(days_remaining)
            elif days_remaining <= (total_sla_days * 0.2):
                app.sla_status = 'near_deadline'
                app.days_left = days_remaining
            else:
                app.sla_status = 'on_time'
                app.days_left = days_remaining
    
    # Statistics - Use localtime for 'today'
    from django.utils import timezone as django_timezone
    today = django_timezone.localtime(django_timezone.now()).date()
    
    # We want ALL assignments stats even if view is filtered
    all_my_assignments = OfficerAssignment.objects.filter(officer=request.user)
    
    stats = {
        'assigned': all_my_assignments.count(),
        'in_progress': all_my_assignments.filter(application__status='under_review').count(),
        'approved_today': all_my_assignments.filter(
            application__status='approved',
            application__approved_date__date=today
        ).count(),
        'pending': all_my_assignments.filter(application__status='pending').count(),
    }
    
    return render(request, 'officer/dashboard_bootstrap.html', {
        'assignments': assignments,
        'stats': stats,
        'filter_type': filter_type
    })

@login_required
@role_required(['officer', 'admin'])
def review_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    
    # Check if assigned to this officer
    if not OfficerAssignment.objects.filter(officer=request.user, application=application).exists() and request.user.role != 'admin':
        messages.error(request, "This application is not assigned to you.")
        return redirect('officer:dashboard')
    
    if request.method == 'POST':
        decision = request.POST.get('decision')
        officer_remarks = request.POST.get('officer_remarks')
        
        if decision == 'approved':
            application.status = 'approved'
            application.approved_by = request.user
            application.approved_date = timezone.now()
            audit_action = 'APP_APPROVE'
            msg = f"Application {application.application_number} approved successfully."
        elif decision == 'rejected':
            application.status = 'rejected'
            application.approved_by = request.user
            application.approved_date = timezone.now()
            audit_action = 'APP_REJECT'
            msg = f"Application {application.application_number} rejected."
        elif decision == 'escalate':
            # Escalation Logic (New)
            audit_action = 'APP_ESCALATE'
            msg = f"Application {application.application_number} escalated to Senior Officer."
            # In a real system, you might change assigned_to here
            # For now, we just log it and maybe keep it under review but needing attention
            if application.remarks:
                application.remarks += f"\n\n[ESCALATED] {request.user.get_full_name()}: {officer_remarks}"
            else:
                application.remarks = f"[ESCALATED] {request.user.get_full_name()}: {officer_remarks}"
            
        else:
            application.status = 'under_review'
            audit_action = 'APP_REVIEW'
            msg = f"Application {application.application_number} marked as under review."
        
        # Append officer remarks to existing remarks
        if officer_remarks and decision != 'escalate':
            if application.remarks:
                application.remarks += f"\n\nOfficer Remarks ({timezone.now().strftime('%Y-%m-%d %H:%M')}): {officer_remarks}"
            else:
                application.remarks = f"Officer Remarks: {officer_remarks}"
        
        application.save()
        
        # Log Audit
        AuditLog.objects.create(
            user=request.user,
            action=audit_action,
            entity_type='Application',
            entity_id=application.id,
            description=f"Application {application.application_number} {decision}. Remarks: {officer_remarks}",
            ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0')
        )
        
        messages.success(request, msg)
        return redirect('officer:dashboard')
    
    # Calculate SLA status
    now = timezone.now()
    time_diff = application.sla_deadline - now
    days_remaining = time_diff.days
    total_sla_days = application.service.processing_days
    
    if days_remaining < 0:
        application.sla_status = 'delayed'
        application.days_overdue = abs(days_remaining)
    elif days_remaining <= (total_sla_days * 0.2):
        application.sla_status = 'near_deadline'
        application.days_left = days_remaining
    else:
        application.sla_status = 'on_time'
        application.days_left = days_remaining
    
    documents = Document.objects.filter(application=application)
    audit_logs = AuditLog.objects.filter(entity_id=application.id, entity_type='Application').order_by('-timestamp')
    
    return render(request, 'officer/review_application_bootstrap.html', {
        'application': application,
        'documents': documents,
        'audit_logs': audit_logs
    })
