from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CitizenRegistrationForm, CustomLoginForm
from django.contrib.auth.decorators import login_required
from core.models import AuditLog

def register_view(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Log Audit
            AuditLog.objects.create(
                user=user,
                action='REGISTER',
                entity_type='User',
                entity_id=user.id,
                description=f"New citizen account created: {user.username}",
                ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0')
            )
            
            login(request, user)
            messages.success(request, f"Welcome {user.first_name if user.first_name else user.username}! Your account has been created.")
            return redirect('citizen:dashboard')
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = CitizenRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Handle 'Remember Me'
            remember_me = request.POST.get('remember_me')
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks in seconds
            else:
                request.session.set_expiry(0)  # Expire on browser close
            
            # Log Audit
            AuditLog.objects.create(
                user=user,
                action='LOGIN',
                entity_type='User',
                entity_id=user.id,
                description=f"User logged in successfully",
                ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0')
            )
            
            messages.success(request, f"Welcome back, {user.first_name if user.first_name else user.username}!")
            
            # Role-based redirection (3-tier architecture routing)
            if user.role == 'citizen':
                return redirect('citizen:dashboard')
            elif user.role == 'officer':
                return redirect('officer:dashboard')
            elif user.role == 'department_head':
                return redirect('mis:dashboard')
            elif user.role == 'admin':
                return redirect('admin_panel:dashboard')
            else:
                return redirect('core:home')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'accounts/login_bootstrap.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('core:home')

@login_required
def profile_view(request):
    from .forms import UserProfileForm
    try:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('accounts:profile')
        else:
            form = UserProfileForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form, 'user': request.user})
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in profile_view: {str(e)}")
        messages.error(request, "There was an error loading your profile. Please try again later.")
        return redirect('core:home')
