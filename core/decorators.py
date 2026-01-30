from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator to restrict access based on user roles.
    Usage: @role_required(['citizen', 'admin'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please login to access this page.")
                return redirect('accounts:login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, f"Access denied. This page is restricted to {', '.join(allowed_roles)} only.")
                # Redirect to appropriate dashboard based on role
                if request.user.role == 'citizen':
                    return redirect('citizen:dashboard')
                elif request.user.role == 'officer':
                    return redirect('officer:dashboard')
                elif request.user.role == 'department_head':
                    return redirect('mis:dashboard')
                elif request.user.role == 'admin':
                    return redirect('admin_panel:dashboard')
                else:
                    return redirect('core:home')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
