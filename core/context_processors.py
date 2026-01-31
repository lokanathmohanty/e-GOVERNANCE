from .models import Notification

def notifications(request):
    try:
        if request.user.is_authenticated:
            notifs = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
            count = Notification.objects.filter(user=request.user, is_read=False).count()
            return {
                'user_notifications': notifs,
                'unread_notification_count': count
            }
    except Exception:
        pass
    return {
        'user_notifications': [],
        'unread_notification_count': 0
    }
