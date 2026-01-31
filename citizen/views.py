from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Application, Service, GrievanceTicket, Document, OfficerAssignment, User, CitizenDocumentLocker
from .forms import ServiceApplicationForm, DocumentUploadForm, GrievanceForm
from django.db import transaction, models
from django.utils import timezone
from core.utils.intelligent_routing import auto_assign_officer
from core.decorators import role_required

@login_required
@role_required(['citizen'])
def dashboard(request):
    from datetime import timedelta
    from django.utils import timezone
    from core.models import Department
    
    applications = Application.objects.filter(user=request.user).select_related('service__department').order_by('-applied_date')
    
    # Calculate SLA status for each application
    now = timezone.now()
    for app in applications:
        try:
            if app.status in ['approved', 'rejected']:
                app.sla_status = 'completed'
            else:
                # Ensure sla_deadline is aware if naive
                deadline = app.sla_deadline
                if timezone.is_naive(deadline):
                    deadline = timezone.make_aware(deadline)
                
                time_diff = deadline - now
                days_remaining = time_diff.days
                total_sla_days = app.service.processing_days
                
                if days_remaining < 0:
                    app.sla_status = 'delayed'
                    app.days_overdue = abs(days_remaining)
                elif days_remaining <= (total_sla_days * 0.2):  # Less than 20% time remaining
                    app.sla_status = 'near_deadline'
                    app.days_left = days_remaining
                else:
                    app.sla_status = 'on_time'
                    app.days_left = days_remaining
        except Exception as e:
            # Fallback for bad data to prevent crash
            app.sla_status = 'unknown'
            app.days_left = 0
    
    # Statistics
    stats = {
        'total': applications.count(),
        'in_progress': applications.filter(status='under_review').count(),
        'approved': applications.filter(status='approved').count(),
        'rejected': applications.filter(status='rejected').count(),
        'delayed': sum(1 for app in applications if hasattr(app, 'sla_status') and app.sla_status == 'delayed')
    }
    
    approved_apps = applications.filter(status='approved')
    departments = Department.objects.all()
    
    # Poll Logic
    active_poll = None
    has_voted = False
    try:
        from core.models import Poll, PollVote
        active_poll = Poll.objects.filter(is_active=True).first()
        if active_poll:
            has_voted = PollVote.objects.filter(user=request.user, poll=active_poll).exists()
    except Exception:
        pass

    # Appointments
    upcoming_appointments = []
    try:
        from core.models import Appointment
        upcoming_appointments = Appointment.objects.filter(user=request.user, date__gte=timezone.now().date()).order_by('date')[:3]
    except Exception:
        pass

    # Smart Reminders
    reminders = []
    try:
        from core.models import CitizenDocumentLocker
        from datetime import timedelta
        expiry_limit = timezone.now().date() + timedelta(days=30)
        reminders = CitizenDocumentLocker.objects.filter(
            user=request.user, 
            expiry_date__lte=expiry_limit,
            expiry_date__gte=timezone.now().date()
        ).order_by('expiry_date')
    except Exception:
        pass
    
    context = {
        'active_poll': active_poll,
        'has_voted': has_voted,
        'upcoming_appointments': upcoming_appointments,
        'reminders': reminders,
        'applications': applications,
        'stats': stats,
        'approved_apps': approved_apps,
        'departments': departments,
    }
    return render(request, 'citizen/dashboard_bootstrap.html', context)

@login_required
def services_list(request):
    from core.models import Department
    services = Service.objects.filter(is_active=True).select_related('department')
    departments = Department.objects.filter(is_active=True)
    return render(request, 'citizen/services_bootstrap.html', {
        'services': services,
        'departments': departments
    })

@login_required
def apply_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    
    # Check restart/resume
    resume_id = request.GET.get('resume')
    existing_app = None
    if resume_id:
        existing_app = Application.objects.filter(id=resume_id, user=request.user, status='draft').first()

    if request.method == 'POST':
        action = request.POST.get('action', 'submit')
        
        with transaction.atomic():
            # Get or Create
            if existing_app:
                application = existing_app
                application.priority = request.POST.get('priority', 'normal')
                application.remarks = request.POST.get('remarks', '')
            else:
                application = Application(
                    user=request.user,
                    service=service,
                    priority=request.POST.get('priority', 'normal'),
                    remarks=request.POST.get('remarks', '')
                )
            
            if action == 'draft':
                application.status = 'draft'
                application.save()
                messages.info(request, "Application saved as draft. You can resume it later.")
                return redirect('citizen:dashboard')
            else:
                application.status = 'pending'
                application.save()
                
                # Save Document
                if 'file_path' in request.FILES and request.POST.get('document_type'):
                    Document.objects.create(
                        application=application,
                        document_type=request.POST.get('document_type'),
                        file_path=request.FILES['file_path'],
                        file_size=request.FILES['file_path'].size
                    )
                
                # Intelligent Routing
                auto_assign_officer(application)
                
                # Audit Log
                from core.models import AuditLog
                AuditLog.objects.create(
                    user=request.user,
                    action='APP_SUBMIT',
                    entity_type='Application',
                    entity_id=application.id,
                    description=f"Citizen submitted application for {service.service_name}",
                    ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0')
                )
                
                messages.success(request, f"Application {application.application_number} submitted successfully!")
                return redirect('citizen:receipt', app_id=application.id)
        
    context = {
        'service': service,
        'existing_app': existing_app
    }
    return render(request, 'citizen/apply_form_bootstrap.html', context)

@login_required
def application_receipt(request, app_id):
    application = get_object_or_404(Application, id=app_id, user=request.user)
    return render(request, 'citizen/receipt.html', {'app': application})

def public_track(request):
    app_number = request.GET.get('app_number')
    application = None
    
    if app_number:
        # Strip whitespace and try to find the application
        app_number_clean = app_number.strip().upper()
        
        # Try exact match first
        application = Application.objects.filter(application_number__iexact=app_number_clean).first()
        
        if not application:
            # Try partial match if exact doesn't work
            application = Application.objects.filter(application_number__icontains=app_number_clean).first()
        
        if not application:
            messages.error(request, f"Application number '{app_number}' not found. Please verify the number and try again.")
            # For debugging - show how many applications exist
            total_apps = Application.objects.count()
            if total_apps > 0:
                messages.info(request, f"Hint: Try copying the exact number from your receipt. System has {total_apps} applications.")
    
    return render(request, 'citizen/search_track.html', {'application': application, 'app_number': app_number})

@login_required
def download_certificate(request, app_id):
    application = get_object_or_404(Application, id=app_id, user=request.user, status='approved')
    from core.utils.certificate_generator import generate_certificate_view
    return generate_certificate_view(request, application)

@login_required
def application_detail(request, app_id):
    application = get_object_or_404(Application, id=app_id, user=request.user)
    documents = application.documents.all()
    
    # Calculate SLA status
    days_left = (application.sla_deadline - timezone.now()).days
    if application.status in ['approved', 'rejected']:
        sla_status = 'completed'
    elif days_left < 0:
        sla_status = 'overdue'
    elif days_left <= 2:
        sla_status = 'near_deadline'
    else:
        sla_status = 'on_time'
        
    return render(request, 'citizen/track.html', {
        'app': application,
        'documents': documents,
        'days_left': days_left,
        'sla_status': sla_status
    })

@login_required
def grievances(request):
    if request.method == 'POST':
        form = GrievanceForm(request.POST, request.FILES)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.user = request.user
            grievance.save()
            messages.success(request, f"Grievance #{grievance.id} submitted successfully!")
            return redirect('citizen:grievances')
    else:
        app_id = request.GET.get('app_id')
        initial = {}
        if app_id:
            initial['application'] = app_id
        form = GrievanceForm(initial=initial)
        form.fields['application'].queryset = Application.objects.filter(user=request.user)
        
    tickets = GrievanceTicket.objects.filter(user=request.user).order_by('-created_at')
    applications_list = Application.objects.filter(user=request.user)
    return render(request, 'citizen/grievance.html', {'form': form, 'tickets': tickets, 'applications_list': applications_list})

@login_required
def document_locker(request):
    from core.models import CitizenDocumentLocker
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            doc_id = request.POST.get('document_id')
            doc = get_object_or_404(CitizenDocumentLocker, id=doc_id, user=request.user)
            doc.delete()
            messages.success(request, "Document removed from locker.")
            return redirect('citizen:locker')
            
        # Upload Logic
        name = request.POST.get('name')
        doc_type = request.POST.get('type')
        file = request.FILES.get('file')
        
        if name and file:
            CitizenDocumentLocker.objects.create(
                user=request.user,
                document_name=name,
                document_type=doc_type,
                file_path=file
            )
            messages.success(request, 'Document permanently added to your locker.')
        else:
            messages.error(request, 'Please provide name and file.')
        return redirect('citizen:locker')
            
    docs = CitizenDocumentLocker.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'citizen/locker.html', {'docs': docs})

@login_required
def submit_feedback(request, app_id):
    from core.models import Feedback
    application = get_object_or_404(Application, id=app_id, user=request.user)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating:
            Feedback.objects.update_or_create(
                application=application,
                defaults={'rating': rating, 'comment': comment}
            )
            messages.success(request, "Thank you for your feedback!")
        else:
            messages.error(request, "Please provide a rating.")
            
    return redirect('citizen:dashboard')

@login_required
def digital_id_card(request):
    return render(request, 'citizen/id_card.html', {'user': request.user})

@login_required
def book_appointment(request):
    from core.models import Department, DepartmentCenter, Appointment, Service
    import random
    
    if request.method == 'POST':
        dept_id = request.POST.get('department')
        center_id = request.POST.get('center')
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        service_id = request.POST.get('service')
        
        dept = get_object_or_404(Department, id=dept_id)
        center = get_object_or_404(DepartmentCenter, id=center_id)
        service = Service.objects.filter(id=service_id).first()
        
        token = f"APT-{random.randint(1000,9999)}"
        
        Appointment.objects.create(
            user=request.user,
            department=dept,
            center=center,
            service=service,
            date=date,
            time_slot=time_slot,
            token_number=token
        )
        messages.success(request, f"Appointment booked successfully! Your Token is {token}")
        return redirect('citizen:appointments')

    departments = Department.objects.all()
    centers = DepartmentCenter.objects.all()
    services = Service.objects.all()
    return render(request, 'citizen/book_appointment.html', {'departments': departments, 'centers': centers, 'services': services})

@login_required
def my_appointments(request):
    from core.models import Appointment
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'citizen/appointments_list.html', {'appointments': appointments})

@login_required
def family_members(request):
    from core.models import FamilyMember
    if request.method == 'POST':
        name = request.POST.get('name')
        relation = request.POST.get('relation')
        dob = request.POST.get('dob')
        aadhaar = request.POST.get('aadhaar')
        
        FamilyMember.objects.create(
            user=request.user,
            name=name,
            relation=relation,
            dob=dob,
            aadhaar_number=aadhaar
        )
        messages.success(request, "Family member added successfully.")
        return redirect('citizen:family')
        
    members = FamilyMember.objects.filter(user=request.user)
    return render(request, 'citizen/family_list.html', {'members': members})

@login_required
def security_dashboard(request):
    from core.models import LoginHistory
    history = LoginHistory.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, 'citizen/security.html', {'history': history})

@login_required
def vote_poll(request, poll_id):
    from core.models import Poll, PollOption, PollVote
    if request.method == 'POST':
        option_id = request.POST.get('option')
        poll = get_object_or_404(Poll, id=poll_id)
        
        if PollVote.objects.filter(user=request.user, poll=poll).exists():
            messages.error(request, "You have already voted.")
        else:
            option = get_object_or_404(PollOption, id=option_id)
            option.votes += 1
            option.save()
            PollVote.objects.create(user=request.user, poll=poll, option=option)
            messages.success(request, "Vote recorded!")
            
    return redirect('citizen:dashboard')
