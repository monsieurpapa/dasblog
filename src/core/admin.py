from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Profile, Category, Tag, Post, Comment, 
    NewsletterSubscription, ContactMessage, Analytics
)

# Unregister the default User admin
admin.site.unregister(User)

# Custom User Admin with Profile inline
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Register User with custom admin
admin.site.register(User, CustomUserAdmin)

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Posts'

# Tag Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Posts'

# Comment Inline for Post Admin
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'content', 'created_at')
    can_delete = True
    show_change_link = True

# Post Admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_date', 'view_count')
    list_filter = ('status', 'category', 'tags', 'published_date')
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ('-published_date', '-created_at')
    inlines = [CommentInline]
    
    fieldsets = (
        ('Post', {
            'fields': ('title', 'slug', 'content', 'summary', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'tags', 'status', 'published_date')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('meta_description', 'meta_keywords', 'canonical_url'),
        }),
    )
    
    def view_count(self, obj):
        return obj.analytics.view_count if hasattr(obj, 'analytics') else 0
    view_count.short_description = 'Views'

# Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'author', 'post', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    actions = ['approve_comments']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} comment(s) approved.")
    approve_comments.short_description = "Approve selected comments"

# Newsletter Subscription Admin
@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    date_hierarchy = 'subscribed_at'
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} subscription(s) activated.")
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} subscription(s) deactivated.")
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"

# Contact Message Admin
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at', 'is_read')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'sent_at'
    readonly_fields = ('name', 'email', 'subject', 'message', 'sent_at')
    
    def has_add_permission(self, request):
        return False  # Prevent adding new messages through admin

# Analytics Admin
@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('post', 'view_count', 'last_viewed')
    list_filter = ('last_viewed',)
    search_fields = ('post__title',)
    date_hierarchy = 'last_viewed'
    readonly_fields = ('view_count', 'last_viewed')
    
    def has_add_permission(self, request):
        return False  # Analytics are created automatically