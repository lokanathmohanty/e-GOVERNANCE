from django.contrib import admin
from .models import User, Department, Service, Application, Document, OfficerAssignment, CitizenDocumentLocker, GrievanceTicket, Feedback, AuditLog, ContactMessage

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'head_officer', 'is_active')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'department', 'is_active')
    list_filter = ('department', 'is_active')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_number', 'user', 'service', 'status', 'priority', 'applied_date')
    list_filter = ('status', 'priority', 'applied_date')
    search_fields = ('application_number', 'user__username')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'department', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at', 'department')
    search_fields = ('name', 'email', 'subject')

admin.site.register(Document)
admin.site.register(OfficerAssignment)
admin.site.register(CitizenDocumentLocker)
admin.site.register(GrievanceTicket)
admin.site.register(Feedback)
admin.site.register(AuditLog)
