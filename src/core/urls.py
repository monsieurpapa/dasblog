from django.urls import path
from . import views
from .views import (
    UserRegisterView, ProfileDetailView, ProfileUpdateView, CommentApproveView, 
    CommentDeleteView, NewsletterUnsubscribeView, ContactMessageListView, 
    ContactMessageDetailView, AnalyticsDashboardView, SearchResultsView
)

app_name = 'core'

urlpatterns = [
    # Home and search
    path('', views.HomeView.as_view(), name='home'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    
    # Posts - Using plural 'posts' as the base for consistency
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<uuid:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<uuid:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<uuid:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/<uuid:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    
    # Categories and Tags
    path('categories/<slug:category_slug>/', views.PostListView.as_view(), name='posts_by_category'),
    path('tags/<slug:tag_slug>/', views.PostListView.as_view(), name='posts_by_tag'),
    
    # User authentication and profiles
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update'),
    
    # Comments
    path('comments/<uuid:pk>/approve/', CommentApproveView.as_view(), name='comment_approve'),
    path('comments/<uuid:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    
    # Contact and Newsletter
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('newsletter/unsubscribe/', NewsletterUnsubscribeView.as_view(), name='newsletter_unsubscribe'),
    
    # Admin and Dashboard
    path('contact-messages/', ContactMessageListView.as_view(), name='contact_message_list'),
    path('contact-messages/<uuid:pk>/', ContactMessageDetailView.as_view(), name='contact_message_detail'),
    path('dashboard/analytics/', AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
]