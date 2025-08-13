from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator  # noqa: F401 (potential future use)
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView  # noqa: F401
from allauth.account.views import LoginView as AllauthLoginView
from django.contrib.auth import login
from .forms import UserRegisterForm, ProfileUpdateForm
from .models import Profile, Post, Category, Tag, Comment, NewsletterSubscription, ContactMessage, Analytics
from .forms import CommentForm, ContactForm, NewsletterForm, PostForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published').order_by('-published_date')
        
        # Filter by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
            
        # Filter by tag
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)
            
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(summary__icontains=query) |
                Q(author__username__icontains=query)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(approved=True)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        # Related posts: same category, exclude current post
        context['related_posts'] = Post.objects.filter(
            category=self.object.category,
            status='published'
        ).exclude(id=self.object.id)[:3]
        # Increment view count or create analytics record
        if self.request.user.is_authenticated:
            analytics, created = Analytics.objects.get_or_create(post=self.object)
            analytics.view_count += 1
            analytics.save()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.status == 'published' and not form.instance.published_date:
            form.instance.published_date = timezone.now()
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        if self.object.status == 'published':
            return reverse_lazy('core:post_detail', kwargs={'pk': self.object.pk})
        return reverse_lazy('core:post_list')



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'summary', 'category', 'tags', 'featured_image', 
              'status', 'meta_description', 'meta_keywords', 'canonical_url']
    
    def form_valid(self, form):
        if form.instance.status == 'published' and not form.instance.published_date:
            form.instance.published_date = timezone.now()
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser
    
    def get_success_url(self):
        return reverse_lazy('core:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('core:post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        # Get the post using the UUID from the URL
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been submitted and is awaiting moderation.')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect back to the post using its UUID
        return reverse_lazy('core:post_detail', kwargs={'pk': self.kwargs['pk']}) + '#comments'


class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('core:contact')
    
    def form_valid(self, form):
        messages.success(self.request, 'Thank you for your message. We will get back to you soon!')
        return super().form_valid(form)


class NewsletterSubscribeView(CreateView):
    model = NewsletterSubscription
    form_class = NewsletterForm
    template_name = 'blog/newsletter_subscribe.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        if NewsletterSubscription.objects.filter(email=email, is_active=True).exists():
            messages.info(self.request, 'This email is already subscribed to our newsletter.')
            return redirect('core:newsletter_subscribe')
        
        messages.success(self.request, 'Thank you for subscribing to our newsletter!')
        return super().form_valid(form)


class NewsletterUnsubscribeView(CreateView):
    model = NewsletterSubscription
    form_class = NewsletterForm
    template_name = 'blog/newsletter_unsubscribe.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        subscription = NewsletterSubscription.objects.filter(email=email, is_active=True).first()
        if subscription:
            subscription.is_active = False
            subscription.save()
            messages.success(self.request, 'You have been unsubscribed from the newsletter.')
        else:
            messages.info(self.request, 'No active subscription found for this email.')
        return super().form_valid(form)


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(summary__icontains=query) |
                Q(author__username__icontains=query),
                status='published'
            ).order_by('-published_date')
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        user = form.save()
        # Create a profile for the new user
        Profile.objects.create(user=user)
        login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return redirect(self.get_success_url())

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'core/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'core/profile_form.html'
    success_url = reverse_lazy('core:profile_detail')

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(status='published').order_by('-published_date')[:6]
        context['categories'] = Category.objects.all()
        context['featured_post'] = Post.objects.filter(status='published', featured_image__isnull=False).order_by('-published_date').first()
        return context


class AccountLoginView(AllauthLoginView):
    template_name = 'auth/login.html'

class CommentApproveView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['approved']
    template_name = 'blog/comment_approve.html'

    def form_valid(self, form):
        messages.success(self.request, 'Comment approved.')
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return self.object.post.get_absolute_url() + '#comments'

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user.is_staff or self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url() + '#comments'

class ContactMessageListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ContactMessage
    template_name = 'blog/contact_message_list.html'
    context_object_name = 'messages_list'
    ordering = ['-sent_at']

    def test_func(self):
        return self.request.user.is_staff

class ContactMessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ContactMessage
    template_name = 'blog/contact_message_detail.html'
    context_object_name = 'message'

    def test_func(self):
        return self.request.user.is_staff

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj

class AnalyticsDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Analytics
    template_name = 'blog/analytics_dashboard.html'
    context_object_name = 'analytics_list'
    paginate_by = 20
    ordering = ['-last_viewed']

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Analytics.objects.select_related('post').order_by('-last_viewed')