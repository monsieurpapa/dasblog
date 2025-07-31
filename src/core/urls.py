from django.urls import path
from . import views
from .views import UserRegisterView, ProfileDetailView, ProfileUpdateView, CommentApproveView, CommentDeleteView, NewsletterUnsubscribeView, ContactMessageListView, ContactMessageDetailView, AnalyticsDashboardView
app_name = 'core'

urlpatterns = [
    # Home and search
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    
    # Posts
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Categories and Tags
    path('category/<slug:category_slug>/', views.PostListView.as_view(), name='posts_by_category'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='posts_by_tag'),
    
    # Comments
    path('post/<slug:slug>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    
    # Contact and Newsletter
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
]

urlpatterns += [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update'),
    path('comment/<uuid:pk>/approve/', CommentApproveView.as_view(), name='comment_approve'),
    path('comment/<uuid:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('newsletter/unsubscribe/', NewsletterUnsubscribeView.as_view(), name='newsletter_unsubscribe'),
    path('admin/messages/', ContactMessageListView.as_view(), name='contact_message_list'),
    path('admin/messages/<uuid:pk>/', ContactMessageDetailView.as_view(), name='contact_message_detail'),
    path('dashboard/analytics/', AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
]