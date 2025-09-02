from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, Tag

class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return Post.objects.none()
            
        # Search in title, content, and tags
        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(summary__icontains=query)
        ).distinct().order_by('-published_date', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        
        # Add search query to context
        context['query'] = query
        
        # Get related categories and tags for filtering
        if query:
            context['related_categories'] = Category.objects.filter(
                post__in=self.get_queryset()
            ).distinct()
            
            context['related_tags'] = Tag.objects.filter(
                post__in=self.get_queryset()
            ).distinct()
        else:
            context['related_categories'] = Category.objects.none()
            context['related_tags'] = Tag.objects.none()
            
        return context
