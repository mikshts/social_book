from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# models from the same app
from .models import (
    User, Profile, Post, Like, Comment,
    Message, AccountDeletionLog, Bookmark
)


# social_book/core/views.py
from .models import Bookmark
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse




from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def run_migrations(request):
    call_command("migrate", interactive=False)
    return HttpResponse("Migrations complete!")




@login_required(login_url='signin')
def index(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        image = request.FILES.get('image')

        if caption or image:
            Post.objects.create(
                user=request.user,
                content=caption,
                caption=caption,
                image=image,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            # 🔒 Redirect to avoid double submission on refresh
            return redirect('index')
        else:
            messages.error(request, "Caption or image is required.")
            return redirect('index')  # 👈 Redirect even on error to prevent resubmission

    # Pagination logic
    all_posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(all_posts, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    bookmarked_post_ids = set(
        Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True)
    )

    for post in page_obj:
        post.liked_users = [like.user for like in post.likes.select_related('user')[:3]]
        post.user_liked = post.likes.filter(user=request.user).exists()
        post.bookmarked = post.id in bookmarked_post_ids

    # AJAX support
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('posts/post_list.html', {'posts': page_obj}, request=request)
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

    return render(request, 'index.html', {'posts': page_obj})

def signup(request):

    if request.method == 'POST':
        signup_username = request.POST['signup-username']#name sang html form auth
        signup_email = request.POST['signup-email']
        signup_password = request.POST['signup-password']
        signup_confirm_password = request.POST['signup-confirm-password']

        if signup_password == signup_confirm_password:
            if User.objects.filter(email=signup_email).exists():
                messages.info(request, 'Email Taken')
                return redirect ('signup')
            elif User.objects.filter(username=signup_username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=signup_username, email=signup_email, password=signup_password)#kwae data para simo html e.g {{user.username}}
                user.save()

                #log user in and redirect to settings page 
                user_login = authenticate(username=signup_username, password=signup_password)
                if user_login is not None:
                    login(request, user_login)
                else:
                    messages.error(request, 'Authentication failed. please try again')
                    return redirect('signup')



                #create a Profile object for new user
            user_model = User.objects.get(username=signup_username)
            Profile.objects.get_or_create(user=user_model)
            return redirect('survey')#pulihi sang first after user login

        else:
            messages.info(request, 'Password is Not Matching')
            return redirect ('signup')
    else:
            return render(request, 'signup.html')
    


def signin(request):
    if request.method == 'POST':
        signin_username = request.POST.get('signin-username')
        signin_password = request.POST.get('signin-password')

        try:
            user_obj = User.objects.get(username=signin_username)
            user_profile, created = Profile.objects.get_or_create(user=user_obj)

            if not user_obj.is_active:
                if user_profile.deactivation_expiry and user_profile.deactivation_expiry > timezone.now():
                    time_remaining = user_profile.deactivation_expiry - timezone.now()
                    days = time_remaining.days
                    seconds_total = int(time_remaining.total_seconds())
                    hours = (seconds_total // 3600) % 24
                    minutes = (seconds_total % 3600) // 60
                    secs = seconds_total % 60

                    formatted_time = ""
                    if days > 0:
                        formatted_time += f"{days} day{'s' if days != 1 else ''}, "
                    formatted_time += f"{hours:02d}:{minutes:02d}:{secs:02d}"

                    messages.error(request, f"Your account is currently deactivated. It will be reactivated in {formatted_time}.")
                    return redirect('signin')
                elif user_profile.deactivation_expiry and user_profile.deactivation_expiry <= timezone.now():
                    user_obj.is_active = True
                    user_obj.save()
                    user_profile.deactivation_expiry = None
                    user_profile.save()
                    messages.success(request, "Your account has been automatically reactivated. Please try logging in again.")
                    return redirect('signin')
                else:
                    messages.error(request, "Your account is currently inactive. Please contact support if you believe this is an error.")
                    return redirect('signin')

        except User.DoesNotExist:
            pass

        user = authenticate(request, username=signin_username, password=signin_password)

        if user is not None:
            user_profile, created = Profile.objects.get_or_create(user=user)
            user_profile.last_login_time = timezone.now()
            user_profile.is_online = True  # ✅ Mark user as online
            user_profile.save()

            login(request, user)
            return redirect('settings')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('signin')

    return render(request, 'signin.html')


@login_required(login_url='signin')
def logout_view(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        user_profile.last_logout_time = timezone.now()
        user_profile.is_online = False  # 🔻 Mark as offline
        user_profile.save()
    except Profile.DoesNotExist:
        pass

    logout(request)
    return redirect('signin')

from django.utils import timezone
from datetime import timedelta

ONLINE_THRESHOLD = timedelta(minutes=5)

def is_user_online(profile):
    if not profile.active_status_date:
        return False
    return timezone.now() - profile.active_status_date < ONLINE_THRESHOLD
def some_view(request):
    profile = Profile.objects.get(user=request.user)
    online_status = is_user_online(profile)
    context = {'profile': profile, 'is_online': online_status}
    return render(request, 'settings.html', context)

@login_required(login_url='signin')
def delete_account(request):
    """
    Handles the deletion of the currently logged-in user's account.
    Logs the deletion event before performing the actual deletion.
    """
    if request.method != 'POST':
        # Only allow POST requests for this action
        return HttpResponse(status=405)  # Method Not Allowed

    # Get the user object that is currently logged in and requesting deletion
    user_to_delete = request.user

    # Get the reason for deletion from the POST data
    reason = request.POST.get('reason', '').strip()

    # Use a database transaction to ensure atomicity:
    # Either both the log entry is created and the user is deleted,
    # or if any error occurs, both operations are rolled back.
    with transaction.atomic():
        try:
            # 1. Log the deletion *before* deleting the account.
            # We record the username of the account being deleted.
            # The 'deleted_by' field points to the current user (who is deleting themselves).
            # Due to on_delete=models.SET_NULL on 'deleted_by', this ForeignKey will become NULL
            # after the user_to_delete.delete() call, which is expected for self-deletion.
            AccountDeletionLog.objects.create(
                deleted_account_username=user_to_delete.username,
                deleted_by=user_to_delete, # This will be the user deleting themselves
                reason=reason if reason else "User self-deleted account." # Use provided reason or a default
            )

            # 2. Log out the user before deleting their account to prevent session issues.
            # This ensures the session is cleared before the user object is gone.
            logout(request) 

            # 3. Perform the actual account deletion.
            # This will trigger CASCADE deletes for related Profile, Post, and Comment objects.
            user_to_delete.delete() 

            messages.success(request, "Your account has been successfully deleted.")
            # Redirect to the sign-in page or a generic success page
            return redirect('signin') 

        except Exception as e:
            # If an error occurs during logging or deletion, the transaction will be rolled back.
            messages.error(request, f"An error occurred while deleting your account: {e}")
            # Redirect back to the settings page or an appropriate error page
            return redirect('settings') # Assuming 'settings' is the URL for your settings page




@login_required(login_url='signin')
def deactivate_account(request):
    if request.method != 'POST':
        return HttpResponse(status=405)  # Method Not Allowed

    deactivation_period = request.POST.get('deactivation_period')
    user_profile = Profile.objects.get(user=request.user)

    # --- IMPORTANT FIX HERE: Ensure user_profile.user.is_active is modified ---
    # In your 30-day block, you had `user_profile.is_active = False`
    # It should be `user_profile.user.is_active = False` to affect Django's User model.
    if deactivation_period == '15':
        expiry_date = timezone.now() + timedelta(days=15)
        user_profile.user.is_active = False # Corrected: affecting the User model
        user_profile.deactivation_expiry = expiry_date
        user_profile.user.save() # Save the Django User model
        user_profile.save() # Save the Profile model
        formatted_expiry = expiry_date.strftime('%Y-%m-%d %H:%M:%S') + f".{int(expiry_date.microsecond / 10000):02d}"
        messages.info(request, f"Your account has been deactivated for 15 days. It will automatically reactivate on {formatted_expiry}.")
        logout(request)
        return redirect('signin')

    elif deactivation_period == '30':
        expiry_date = timezone.now() + timedelta(days=30)
        user_profile.user.is_active = False # FIX APPLIED HERE: affecting the User model
        user_profile.deactivation_expiry = expiry_date
        user_profile.user.save() # Save the Django User model
        user_profile.save() # Save the Profile model
        formatted_expiry = expiry_date.strftime('%Y-%m-%d %H:%M:%S') + f".{int(expiry_date.microsecond / 10000):02d}"
        messages.info(request, f"Your account has been deactivated for 30 days. It will automatically reactivate on {formatted_expiry}.")
        logout(request)
        return redirect('signin')

    else:
        messages.error(request, "Invalid deactivation period selected.")
        return redirect('settings')
#### delete if needed
# views.py


@login_required(login_url='signin')
def add_comment(request, post_id):
    # This view will just validate CSRF and return OK
    if request.method == 'POST':
        return JsonResponse({'status': 'validated'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
 
 
# List all posts
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})


# View a single post
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('created_at')
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments})

# Create a post from standalone page
@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post = Post.objects.create(
                user=request.user,
                content=content,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                no_of_likes=0
            )
            messages.success(request, "Post created successfully.")
            return redirect('index', post_id=post.id)
        else:
            messages.error(request, "Content cannot be empty.")
    return render(request, 'posts/create_post.html')


@login_required
@csrf_exempt
def delete_post(request, post_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'}, status=404)

    if post.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

    # ✅ Store data BEFORE deleting
    post_data = {
        'post_id': str(post.id),
        'username': post.user.username,
    }

    post.delete()

    # ✅ WebSocket broadcast
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "posts_feed",
        {
            "type": "broadcast_post_delete",
            **post_data,
        }
    )

    return JsonResponse({'status': 'success', **post_data})



@csrf_exempt
@require_POST
def create_post_from_index(request):
    caption = request.POST.get("caption")
    image = request.FILES.get("image")

    post = Post.objects.create(user=request.user, caption=caption, image=image)

    # Render the post HTML using Django template
    post_html = render_to_string("posts/post_single.html", {
        "post": post,
        "user": request.user,  # Needed for {% if user == post.user %}
    })

    # Notify WebSocket group with rendered HTML
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "posts_feed",
        {
            "type": "new_post",
            "html": post_html,
        }
    )

    return JsonResponse({"status": "success"})


#LIKE REACT POST ---------------------------------------------------------------------------------


@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        like.delete()

    post.no_of_likes = post.likes.count()
    post.save()

    recent_likers = post.likes.select_related('user__profile').order_by('-id')[:3]
    liker_data = [
        {
            'username': liker.user.username,
            'profile_img': liker.user.profile.profileimg.url
        }
        for liker in recent_likers
    ]

    # WebSocket Broadcast (fix UUID serialization issue)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'post_{str(post.id)}',  # Ensure post.id is a string
        {
            'type': 'send_like_update',
            'post_id': str(post.id),  # Convert UUID to string
            'likes_count': post.no_of_likes,
            'recent_likers': liker_data
        }
    )

    return JsonResponse({
        'status': 'liked' if created else 'unliked',
        'likes_count': post.no_of_likes,
        'recent_likers': liker_data
    })


# views.py
# views.py




@login_required
def profile_view(request):
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    # Initialize errors dict with empty lists for each field
    errors = {
        'location': [],
        'relation': [],
        'gender': [],
        'bio': [],
        'age': [],
        'height': [],
        'weight': [],
        'birthday': [],
        'profile_img': [],
    }

    if request.method == 'POST':
        # Location validation
        location = request.POST.get('location', '').strip()
        if len(location) > 100:
            errors['location'].append("Location must be 100 characters or less.")
        else:
            profile.location = location

        # Relationship validation
        relation = request.POST.get('relation', '').strip()
        if relation and relation not in dict(Profile.RELATIONSHIP_CHOICES):
            errors['relation'].append("Invalid relationship status selected.")
        else:
            profile.relation = relation

        # Gender validation
        gender = request.POST.get('gender', '').strip()
        if gender and gender not in dict(Profile.GENDER_CHOICES):
            errors['gender'].append("Invalid gender selected.")
        else:
            profile.gender = gender

        # Bio validation
        bio = request.POST.get('bio', '').strip()
        if len(bio) > 1000:
            errors['bio'].append("Bio must be 1000 characters or less.")
        else:
            profile.bio = bio

        # Age validation
        age_str = request.POST.get('age', '').strip()
        if age_str:
            try:
                age = int(age_str)
                if age < 13 or age > 120:
                    errors['age'].append("Age must be between 13 and 120.")
                else:
                    profile.age = age
            except ValueError:
                errors['age'].append("Age must be a valid number.")
        else:
            profile.age = None

        # Height validation
        height_str = request.POST.get('height', '').strip()
        if height_str:
            try:
                height = Decimal(height_str)
                if height < 1 or height > 10:
                    errors['height'].append("Height must be between 1 and 10 feet.")
                else:
                    profile.height = height
            except (ValueError, InvalidOperation):
                errors['height'].append("Height must be a valid decimal number.")
        else:
            profile.height = None

        # Weight validation (must be in kg)
       # Weight validation (must be in kg)
        weight_str = request.POST.get('weight', '').strip()
        if weight_str:
            try:
                weight = Decimal(weight_str)
                if not (Decimal('30') <= weight <= Decimal('500')):
                    errors['weight'].append("Weight must be between 30 and 500 kg.")
                else:
                    profile.weight = weight
            except (ValueError, InvalidOperation):
                errors['weight'].append("Weight must be a valid number in kg (e.g. 55.5).")
        else:
            profile.weight = None


        # Birthday validation
        birthday_str = request.POST.get('birthday', '').strip()
        if birthday_str:
            try:
                birthday = parse_date(birthday_str)
                from datetime import date
                today = date.today()
                if birthday is None:
                    errors['birthday'].append("Invalid birthday format. Use MM-DD-YYYY.")
                else:
                    age_from_birthday = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
                    if birthday > today:
                        errors['birthday'].append("Birthday cannot be in the future.")
                    elif age_from_birthday < 13:
                        errors['birthday'].append("You must be at least 13 years old.")
                    elif age_from_birthday > 120:
                        errors['birthday'].append("Please enter a valid birthday.")
                    else:
                        profile.birthday = birthday
            except Exception:
                errors['birthday'].append("Invalid birthday format.")
        else:
            profile.birthday = None

        # Profile image upload
        if 'profile_img' in request.FILES:
            profile_img = request.FILES['profile_img']
            if profile_img.size > 5 * 1024 * 1024:
                errors['profile_img'].append("Profile image must be less than 5MB.")
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if profile_img.content_type not in allowed_types:
                errors['profile_img'].append("Profile image must be JPEG, PNG, or GIF format.")
            if not any(errors.values()):  # No errors in any field
                profile.profileimg = profile_img

        # Check if there are any errors collected
        has_errors = any(errors[field] for field in errors)

        if not has_errors:
            try:
                profile.full_clean()
                profile.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')
            except ValidationError as e:
                # Assign model validation errors to fields
                for field, field_errors in e.message_dict.items():
                    if field in errors:
                        errors[field].extend(field_errors)
                messages.error(request, "Please correct the errors below.")
            except Exception:
                messages.error(request, "An unexpected error occurred. Please try again.")

        else:
            # Add all errors to messages so they display at top
            for field_errors in errors.values():
                for err in field_errors:
                    messages.error(request, err)

    # For GET or after POST failure, prepare current_values for form
    current_values = {
        'location': profile.location or '',
        'relation': profile.relation or '',
        'gender': profile.gender or '',
        'bio': profile.bio or '',
        'age': profile.age or '',
        'height': profile.height or '',
        'weight': profile.weight or '',
        'birthday': profile.birthday.isoformat() if profile.birthday else '',
        'profile_img_url': profile.profileimg.url if profile.profileimg else '',
    }

    context = {
        'current_values': current_values,
        'errors': {k: v[0] if v else None for k, v in errors.items()},  # Show first error per field in template
        'relationship_choices': Profile.RELATIONSHIP_CHOICES,
        'gender_choices': Profile.GENDER_CHOICES,
    }

    return render(request, 'settings.html', context)



class ProfileForm(forms.ModelForm):
    """
    Form for handling profile updates with built-in validation
    """
    class Meta:
        model = Profile
        fields = [
            'bio', 'profileimg', 'location', 'age', 'relation', 
            'gender', 'height', 'weight', 'birthday'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'maxlength': 1000}),
            'location': forms.TextInput(attrs={'maxlength': 100}),
            'age': forms.NumberInput(attrs={'min': 13, 'max': 120}),
            'height': forms.NumberInput(attrs={'step': '0.1', 'min': '1', 'max': '10'}),
            'weight': forms.NumberInput(attrs={'step': '0.1', 'min': '30', 'max': '500'}),
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'relation': forms.Select(),
            'gender': forms.Select(),
        }
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 13 or age > 120):
            raise forms.ValidationError("Age must be between 13 and 120.")
        return age
    
    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday:
            from datetime import date
            today = date.today()
            if birthday > today:
                raise forms.ValidationError("Birthday cannot be in the future.")
            
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
            if age < 13:
                raise forms.ValidationError("You must be at least 13 years old.")
            elif age > 120:
                raise forms.ValidationError("Please enter a valid birthday.")
        return birthday
    
    def clean_profileimg(self):
        image = self.cleaned_data.get('profileimg')
        if image:
            # Validate file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large (max 5MB).")
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if image.content_type not in allowed_types:
                raise forms.ValidationError("Please upload a valid image file (JPEG, PNG, or GIF).")
        
        return image


@login_required 
def profile_view_with_forms(request):
    """
    Alternative implementation using Django Forms (Recommended)
    """
    user = request.user
    
    # Get or create profile
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            # Form errors will be displayed in the template
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'user_profile': profile,
    }
    
    return render(request, 'settings.html', context)

# core/views.py

@login_required
def chat_view(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)

    # Fetch past messages between the current user and the receiver
    # This queries messages where:
    # (sender is current_user AND receiver is target_receiver) OR
    # (sender is target_receiver AND receiver is current_user)
    past_messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp') # Order by timestamp to display chronologically

    context = {
        'receiver': receiver,
        'past_messages': past_messages,
    }
    return render(request, 'chat.html', context)

@login_required(login_url='signin')
def settings(request):
    survey_data = None
    if request.user.is_authenticated:
        try:
            survey_data = request.user.survey  # Access the OneToOne relationship
        except:
            pass
    return render(request, 'settings.html', {'survey': survey_data})


def about(request):
    return render(request, 'about.html')

def analytics(request):
    return render(request, 'analytics.html')


def explore(request):
    return render(request, 'explore.html')

def forgotpass(request):
    return render(request, 'forgotpass.html')

def help(request):
    return render(request, 'help.html')


def services(request):
    return render(request, 'services.html')


def terms(request):
    return render(request, 'terms.html')


def profile(request):
    return render(request, 'profile.html')



def search_users(request):
    query = request.GET.get('q', '').strip()
    profiles = Profile.objects.none()

    if query:
        exact = Profile.objects.filter(user__username__iexact=query)

        starts_with = Profile.objects.filter(
            user__username__istartswith=query
        ).exclude(pk__in=exact.values_list('pk', flat=True))

        contains = Profile.objects.filter(
            user__username__icontains=query
        ).exclude(pk__in=exact.values_list('pk', flat=True)).exclude(pk__in=starts_with.values_list('pk', flat=True))

        profiles = list(exact) + list(starts_with) + list(contains)

    return render(request, 'search.html', {
        'query': query,
        'profiles': profiles,
    })



User = get_user_model()

def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'profile.html', {'profile': profile})



#survey/views.py
from django.shortcuts import render, redirect
from .models import UserSurvey

@login_required(login_url='signin')
def survey(request):
    if request.method == "POST":
        # --- Page 1 ---
        gender = request.POST.getlist('gender')
        looking_for = request.POST.getlist('looking_for')
        age_range = request.POST.getlist('age_range')

        # --- Page 2 ---
        goal = request.POST.getlist('goal')
        meet = request.POST.getlist('meet')

        # --- Page 3 ---
        smoke = request.POST.getlist('smoke')
        drink = request.POST.getlist('drink')
        children = request.POST.getlist('children')
        hobbies = request.POST.getlist('hobbies')

        # --- Page 4 ---
        traits = request.POST.getlist('traits')
        love_language = request.POST.getlist('love_language')

        # Save to DB (overwrites if already exists)
        UserSurvey.objects.update_or_create(
            user=request.user,
            defaults={
                'gender': gender,
                'looking_for': looking_for,
                'age_range': age_range,
                'goal': goal,
                'meet': meet,
                'smoke': smoke,
                'drink': drink,
                'children': children,
                'hobbies': hobbies,
                'traits': traits,
                'love_language': love_language,
            }
        )

        return redirect('settings')  # ✅ Redirect to settings.html

    return render(request, 'survey.html')

#bookmarks/views.py----


@login_required
def toggle_bookmark(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)

        if not created:
            bookmark.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.utils.timezone import now

from django.utils.timezone import now

@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('post__user', 'post__user__profile')

    liked_post_ids = set(
        request.user.like_set.values_list('post_id', flat=True)
    )

    # Attach custom attributes to each bookmark
    for bookmark in bookmarks:
        bookmark.is_online = bookmark.post.user.profile.is_online
        bookmark.is_liked = bookmark.post.id in liked_post_ids

    return render(request, 'bookmarks.html', {
        'bookmarks': bookmarks,
    })


#end of bookmarks ---
def post_detail_modal(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail_modal.html', {'post': post})

# friend_requests/views.py____________-------------ubrahunin -------_____________
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import FriendRequest, Profile
from django.contrib.auth.models import User

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    if not created:
        return JsonResponse({'status': 'already_sent'})
    return JsonResponse({'status': 'request_sent'})

@login_required
def respond_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.to_user != request.user:
        return JsonResponse({'status': 'unauthorized'}, status=403)

    action = request.POST.get("action")

    if action == "accept":
        friend_request.is_accepted = True
        friend_request.save()
        return JsonResponse({'status': 'accepted'})
    elif action == "decline":
        friend_request.delete()
        return JsonResponse({'status': 'declined'})
    return JsonResponse({'status': 'invalid_action'}, status=400)


from django.contrib.auth.decorators import login_required
from django.db.models import Max, Q
from .models import Message, Profile, User

@login_required
def message_list_view(request):
    user = request.user

    # Get the latest message per conversation partner
    latest_messages = (
        Message.objects.filter(Q(sender=user) | Q(receiver=user))
        .order_by('receiver', '-timestamp')
        .distinct('receiver')  # Works in PostgreSQL
    )

    # For SQLite/MySQL, manually filter latest message per partner:
    # Optionally, group by each user, then get the latest message using a loop if necessary.

    context = {
        'messages': latest_messages,
    }
    return render(request, 'partials/message_list.html', context)



from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Message

@login_required
def recent_messages(request):
    user = request.user

    # Get latest message per conversation partner
    # Step 1: Get all messages involving current user
    all_messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-timestamp')

    # Step 2: Track latest message per unique user pair
    seen_users = set()
    recent_conversations = []

    for msg in all_messages:
        other_user = msg.receiver if msg.sender == user else msg.sender
        if other_user.id not in seen_users:
            seen_users.add(other_user.id)
            recent_conversations.append({
                "user": other_user,
                "message": msg,
            })

    return render(request, 'partials/message_list.html', {"conversations": recent_conversations})
