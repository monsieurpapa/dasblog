from django.urls import path
from . import analytics_views

app_name = 'analytics'

urlpatterns = [
    path('', analytics_views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('post/<uuid:pk>/', analytics_views.PostAnalyticsView.as_view(), name='post_analytics'),
]
