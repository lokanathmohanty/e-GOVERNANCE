from django.db.models import Count, Q
from core.models import User, OfficerAssignment

def auto_assign_officer(application):
    """
    Intelligent routing: Assigns application to the officer with the least current workload.
    """
    officers = User.objects.filter(role='officer', is_active=True)
    
    officer = officers.annotate(
        workload=Count('assigned_tasks', filter=Q(assigned_tasks__application__status__in=['pending', 'under_review']))
    ).order_by('workload').first()
    
    if officer:
        OfficerAssignment.objects.create(
            officer=officer,
            application=application
        )
        return officer
    return None
