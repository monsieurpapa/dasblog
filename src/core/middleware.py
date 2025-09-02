import logging
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from .models import Analytics, Post

logger = logging.getLogger(__name__)

class AnalyticsMiddleware:
    """
    Middleware to track post views and update analytics.
    Uses caching to prevent database hits on every request.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = [
            '/admin/',
            '/static/',
            '/media/',
            '/favicon.ico',
        ]

    def __call__(self, request):
        response = self.get_response(request)
        
        # Skip tracking for certain paths
        if any(request.path.startswith(path) for path in self.exempt_paths):
            return response
            
        # Only track GET requests
        if request.method == 'GET' and hasattr(request, 'resolver_match'):
            try:
                self._track_post_view(request)
            except Exception as e:
                logger.error(f"Error in AnalyticsMiddleware: {str(e)}", exc_info=True)
                
        return response
    
    def _track_post_view(self, request):
        """Track a view of a post if the current URL is a post detail page."""
        # Check if this is a post detail view
        if not hasattr(request, 'resolver_match') or not request.resolver_match:
            return
            
        view_name = request.resolver_match.view_name
        if view_name != 'core:post_detail':
            return
            
        # Get the post ID from URL kwargs
        post_id = request.resolver_match.kwargs.get('pk')
        if not post_id:
            return
            
        # Create a unique cache key for this user + post
        cache_key = f'post_view:{post_id}:{request.META.get("REMOTE_ADDR")}'
        
        # Check if this view has been tracked recently (5 minute window)
        if cache.get(cache_key):
            return
            
        # Set a cache entry to prevent duplicate tracking
        cache.set(cache_key, True, 300)  # 5 minutes
        
        # Use atomic update to prevent race conditions
        analytics, created = Analytics.objects.get_or_create(
            post_id=post_id,
            defaults={'view_count': 0}
        )
        
        # Update view count
        from django.db.models import F
        Analytics.objects.filter(pk=analytics.pk).update(
            view_count=F('view_count') + 1,
            last_viewed=timezone.now()
        )
