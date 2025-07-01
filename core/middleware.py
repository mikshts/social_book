# myapp/middleware.py

from django.utils import timezone
from django.conf import settings
from .models import Profile

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                profile.active_status_date = timezone.now()
                profile.is_online = True
                profile.save(update_fields=['active_status_date', 'is_online'])
            except Profile.DoesNotExist:
                pass

        return response
