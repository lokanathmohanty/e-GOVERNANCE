from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        return {
            'user_notifications': Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5],
            'unread_notification_count': Notification.objects.filter(user=request.user, is_read=False).count()
        }
    return {}
