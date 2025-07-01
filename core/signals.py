from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver to create a Profile instance whenever a new User is created.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Signal receiver to save the Profile instance whenever the User instance is saved.
    This ensures that if a User is updated, its associated Profile is also considered for saving.
    """
    # Ensure a profile exists before trying to save it
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(user_logged_in)
def update_active_status_on_login(sender, request, user, **kwargs):
    """
    Signal receiver to update the active_status_date on user login.
    """
    try:
        profile = Profile.objects.get(user=user)
        profile.active_status_date = timezone.now()
        profile.save()
    except Profile.DoesNotExist:
        # This case should ideally not happen if create_profile signal works correctly,
        # but it's good for robustness.
        print(f"Warning: Profile not found for user {user.username} during login.")

@receiver(user_logged_out)
def update_active_status_on_logout(sender, request, user, **kwargs):
    """
    Signal receiver to update the active_status_date on user logout.
    """
    try:
        profile = Profile.objects.get(user=user)
        profile.active_status_date = timezone.now()
        profile.save()
    except Profile.DoesNotExist:
        print(f"Warning: Profile not found for user {user.username} during logout.")