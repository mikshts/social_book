from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# ---------------------------
# Profile
# ---------------------------
class Profile(models.Model):
    RELATIONSHIP_CHOICES = [
        ('single', 'Single'),
        ('in_a_relationship', 'In a Relationship'),
        ('married', 'Married'),
        ('complicated', "It's Complicated"),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('gay', 'Gay'),
        ('lesbian', 'Lesbian'),
        ('neutral', 'Neutral'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(
        upload_to='profile_images/',
        default='https://res.cloudinary.com/.../blank_profile_picture.png',
        max_length=500
    )
    location = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    relation = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    deactivation_expiry = models.DateTimeField(null=True, blank=True)
    active_status_date = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def can_login(self):
        if not self.is_active and self.deactivation_expiry:
            if timezone.now() > self.deactivation_expiry:
                self.is_active = True
                self.deactivation_expiry = None
                self.save()
                return True
            return False
        return self.is_active


# ---------------------------
# Post, Like, Comment, Bookmark
# ---------------------------
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    no_of_likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def total_bookmarks(self):
        return self.bookmark_set.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} liked {self.post}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.id}"


# ---------------------------
# Messaging
# ---------------------------
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username} ({self.timestamp.strftime('%H:%M')})"


# ---------------------------
# Friend Requests
# ---------------------------
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({'Accepted' if self.is_accepted else 'Pending'})"


# ---------------------------
# Survey
# ---------------------------
class UserSurvey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="survey")

    # Page 1 - Basic Info
    gender = models.JSONField(default=list, blank=True)
    looking_for = models.JSONField(default=list, blank=True)
    age_range = models.JSONField(default=list, blank=True)

    # Page 2 - Relationship Goals
    goal = models.JSONField(default=list, blank=True)
    meet = models.JSONField(default=list, blank=True)

    # Page 3 - Lifestyle
    smoke = models.JSONField(default=list, blank=True)
    drink = models.JSONField(default=list, blank=True)
    children = models.JSONField(default=list, blank=True)
    hobbies = models.JSONField(default=list, blank=True)

    # Page 4 - Personality
    traits = models.JSONField(default=list, blank=True)
    love_language = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Survey of {self.user.username}"


# ---------------------------
# Account Deletion Log
# ---------------------------
class AccountDeletionLog(models.Model):
    deleted_account_username = models.CharField(
        max_length=150,
        help_text="Username of the account that was deleted."
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='account_deletion_records',
        help_text="The user who performed the account deletion (null = self-deletion)."
    )
    deletion_timestamp = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Account Deletion Log"
        verbose_name_plural = "Account Deletion Logs"
        ordering = ['-deletion_timestamp']

    def __str__(self):
        deleter_info = self.deleted_by.username if self.deleted_by else "Self-deleted / System"
        return f"{self.deleted_account_username} deleted by {deleter_info} on {self.deletion_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
