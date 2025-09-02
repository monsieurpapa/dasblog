from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, TemplateView
from django.db.models import Count, Sum, F, Case, When, IntegerField
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.utils import timezone
from datetime import timedelta
from .models import Post, Analytics, Comment

class AnalyticsDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/dashboard.html'
    login_url = 'account_login'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Time period for analytics (last 30 days)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Get top posts by views
        top_posts = Post.objects.filter(
            analytics__last_viewed__range=(start_date, end_date)
        ).annotate(
            view_count=Sum('analytics__view_count')
        ).order_by('-view_count')[:10]
        
        # Get views by day for the last 30 days
        daily_views = Analytics.objects.filter(
            last_viewed__range=(start_date, end_date)
        ).annotate(
            date=TruncDate('last_viewed')
        ).values('date').annotate(
            views=Sum('view_count')
        ).order_by('date')
        
        # Get recent comments
        recent_comments = Comment.objects.filter(
            created_at__range=(start_date, end_date)
        ).select_related('post', 'author').order_by('-created_at')[:10]
        
        # Get views by post category
        category_views = Post.objects.filter(
            analytics__last_viewed__range=(start_date, end_date)
        ).values('category__name').annotate(
            views=Sum('analytics__view_count'),
            post_count=Count('id', distinct=True)
        ).order_by('-views')
        
        context.update({
            'top_posts': top_posts,
            'daily_views': list(daily_views),
            'recent_comments': recent_comments,
            'category_views': category_views,
            'start_date': start_date,
            'end_date': end_date,
        })
        
        return context

class PostAnalyticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/post_analytics.html'
    login_url = 'account_login'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('pk')
        
        try:
            post = Post.objects.get(pk=post_id)
            
            # Time period for analytics (last 30 days)
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
            
            # Get daily views for this post
            daily_views = Analytics.objects.filter(
                post=post,
                last_viewed__range=(start_date, end_date)
            ).annotate(
                date=TruncDate('last_viewed')
            ).values('date').annotate(
                views=Sum('view_count')
            ).order_by('date')
            
            # Get views by week
            weekly_views = Analytics.objects.filter(
                post=post,
                last_viewed__range=(start_date, end_date)
            ).annotate(
                week=TruncWeek('last_viewed')
            ).values('week').annotate(
                views=Sum('view_count')
            ).order_by('week')
            
            context.update({
                'post': post,
                'daily_views': list(daily_views),
                'weekly_views': list(weekly_views),
                'start_date': start_date,
                'end_date': end_date,
            })
            
        except Post.DoesNotExist:
            pass
            
        return context
