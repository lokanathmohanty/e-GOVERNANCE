from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
import os

class User(AbstractUser):
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('officer', 'Officer'),
        ('department_head', 'Department Head'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    description = models.TextField()
    head_officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='headed_departments')
    contact_email = models.EmailField()
    is_active = models.BooleanField(default=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name

class Service(models.Model):
    service_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='services')
    description = models.TextField()
    required_documents = models.TextField(help_text="Comma separated list of required documents")
    processing_days = models.IntegerField(default=7, help_text="SLA in days")
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service_name} ({self.department.department_name})"

class Application(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    PRIORITY_CHOICES = (
        ('normal', 'Normal'),
        ('emergency', 'Emergency'),
        ('disaster', 'Disaster'),
    )
    application_number = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    remarks = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_applications')
    approved_date = models.DateTimeField(null=True, blank=True)
    sla_deadline = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.application_number:
            # Generate APP-YYYY-DEPT-UUID
            from django.utils import timezone
            year = timezone.now().year
            dept_code = self.service.department.department_name[:3].upper()
            unique_id = uuid.uuid4().hex[:6].upper()
            self.application_number = f"APP-{year}-{dept_code}-{unique_id}"
        
        if not self.sla_deadline:
            from datetime import timedelta
            from django.utils import timezone
            self.sla_deadline = timezone.now() + timedelta(days=self.service.processing_days)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.application_number

class Document(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100)
    file_path = models.FileField(upload_to='documents/applications/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.document_type} for {self.application.application_number}"

class OfficerAssignment(models.Model):
    officer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'officer'}, related_name='assigned_tasks')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='officer_assignments')
    assigned_date = models.DateTimeField(auto_now_add=True)
    workload_at_assignment = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.officer.username} assigned to {self.application.application_number}"

class CitizenDocumentLocker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_locker')
    document_name = models.CharField(max_length=100)
    document_type = models.CharField(max_length=100)
    file_path = models.FileField(upload_to='locker/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.document_name} ({self.user.username})"

class GrievanceTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    CATEGORY_CHOICES = (
        ('sanitation', 'Sanitation'),
        ('electricity', 'Electricity'),
        ('water', 'Water Supply'),
        ('road', 'Road Maintenance'),
        ('other', 'Other'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grievances')
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=(('normal', 'Normal'), ('high', 'High')), default='normal')
    attachment = models.FileField(upload_to='grievance_attachments/', null=True, blank=True)
    escalation_level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"GRV-{self.id}: {self.subject}"

class Feedback(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.application.application_number} - {self.rating} Stars"

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'User Login'),
        ('LOGOUT', 'User Logout'),
        ('REGISTER', 'User Registration'),
        ('APP_CREATE', 'Application Created'),
        ('APP_APPROVE', 'Application Approved'),
        ('APP_REJECT', 'Application Rejected'),
        ('DOC_UPLOAD', 'Document Uploaded'),
        ('GRIEV_CREATE', 'Grievance Created'),
        ('USER_CREATE', 'User Created (Admin)'),
        ('DEPT_MODIFY', 'Department Modified'),
        ('SERVICE_MODIFY', 'Service Modified'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=50)  # 'Application', 'Grievance', etc.
    entity_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError("Audit logs cannot be modified")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise ValueError("Audit logs cannot be deleted")

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    attachment = models.FileField(upload_to='contact_attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.name}"

class Notification(models.Model):
    TYPES = (
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

# --- Appointments ---
class DepartmentCenter(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    center = models.ForeignKey(DepartmentCenter, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time_slot = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='scheduled')
    token_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

# --- Family Profiles ---
class FamilyMember(models.Model):
    RELATIONS = (('Spouse', 'Spouse'), ('Child', 'Child'), ('Parent', 'Parent'), ('Sibling', 'Sibling'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_members')
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=20, choices=RELATIONS)
    dob = models.DateField()
    aadhaar_number = models.CharField(max_length=12, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.relation})"

# --- Login History ---
class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

# --- Polls ---
class Poll(models.Model):
    question = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.question

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
    def __str__(self): return self.text

class PollVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'poll')

class Announcement(models.Model):
    CATEGORY_CHOICES = (
        ('news', 'News & Updates'),
        ('circular', 'Circular & Notice'),
        ('alert', 'Emergency Alert'),
        ('broadcast', 'Emergency Broadcast Mode'),
        ('policy', 'Policy Update'),
        ('internal', 'Internal Memo (Staff Only)'),
    )
    PRIORITY_CHOICES = (
        ('normal', 'Normal'),
        ('high', 'High / Critical'),
        ('emergency', 'Life-Safety / Immediate'),
    )
    
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='news')
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='normal')
    target_role = models.CharField(max_length=20, blank=True, null=True, help_text="Specific role to target (optional)")
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='announcements/images/', blank=True, null=True)
    document = models.FileField(upload_to='announcements/docs/', blank=True, null=True, help_text="PDF or Document for download")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
        
    def __str__(self):
        return self.title

class SystemConfiguration(models.Model):
    # Global Config
    ENVIRONMENT_CHOICES = (('dev', 'Development'), ('staging', 'Staging'), ('prod', 'Production'))
    environment = models.CharField(max_length=10, choices=ENVIRONMENT_CHOICES, default='dev')
    maintenance_mode = models.BooleanField(default=False)
    
    # Branding
    portal_name = models.CharField(max_length=100, default='e-Governance Portal')
    primary_color = models.CharField(max_length=7, default='#007bff')
    
    # Global Rules
    max_upload_size_mb = models.IntegerField(default=5)
    global_sla_days = models.IntegerField(default=7)
    
    # Feature Toggles
    enable_grievances = models.BooleanField(default=True)
    enable_appointments = models.BooleanField(default=True)
    enable_notifications = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    system_version = models.CharField(max_length=20, default='2.4.0-build.82')
    maintenance_end_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "System Configuration"
        verbose_name_plural = "System Configuration"

    def __str__(self):
        return f"System Config ({self.environment})"
