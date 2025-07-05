from django.urls import path
from . import views
from .views import profile_view
from django.contrib import admin
from .views import chat_view

urlpatterns = [

    path('', views.index, name='index'),
    path('settings/', profile_view, name='profile'),
    path('chat/<int:receiver_id>/', chat_view, name='chat'),
    path('recent-messages/', views.recent_messages, name='recent_messages'),

        # Survey
    path('survey/', views.survey, name='survey'),
    path('toggle_bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.bookmark_list, name='bookmarks'),
    # friend requests
    path('friend-request/send/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friend-request/respond/<int:request_id>/', views.respond_friend_request, name='respond_friend_request'),
    # Messaging

        


    # auth
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('forgotpass/', views.forgotpass, name='forgotpass'),
    path('settings/', views.settings, name='settings'),

    # legal
    path('logout/', views.logout_view, name='logout_view'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('deactivate/', views.deactivate_account, name='deactivate_account'),

    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('help/', views.help, name='help'),
    path('services/', views.services, name='services'),

    # sidebars
    path('analaytics/', views.analytics, name='analytics'),
    path('explore/', views.explore, name='explore'),

    # nav
    path('profile/', views.profile, name='profile'),
    path('search-users/', views.search_users, name='search-users'),

    # post-related URLs (feed and posts)
    path('post_list/', views.post_list, name='post_list'),  # Feed page
    path('post/<uuid:post_id>/', views.post_detail, name='post_detail'),  # Individual post
    path('post/create/', views.create_post, name='create_post'),  # Create from dedicated page
    path('post/<uuid:post_id>/delete/', views.delete_post, name='delete_post'),
    path("post/modal/create/", views.create_post_from_index, name="create_post_from_index"),
    path('post/<uuid:post_id>/comment/', views.add_comment, name='add_comment'),
    path('like/<uuid:post_id>/', views.like_post, name='like-post'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),
    path('post_detail_modal/<uuid:post_id>/', views.post_detail_modal, name='post_detail_modal'),

]

    



