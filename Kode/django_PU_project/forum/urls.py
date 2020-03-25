from django.urls import path, re_path
from .views import (
    ThreadListView, 
    ThreadDetailView, 
    ThreadCreateView, 
    ThreadUpdateView, 
    ThreadDeleteView, 
    UserThreadListView,
    GiveVote
)
from . import views

from updown.views import AddRatingFromModel


urlpatterns = [
    path('', ThreadListView.as_view(), name='forum-home'),
    path('user/<str:username>', UserThreadListView.as_view(), name='user-threads'),
    path('thread/<int:pk>/', ThreadDetailView.as_view(), name='thread-detail'),
    path('thread/new/', ThreadCreateView.as_view(), name='thread-create'),
    path('thread/<int:pk>/update/', ThreadUpdateView.as_view(), name='thread-update'),
    path('thread/<int:pk>/delete/', ThreadDeleteView.as_view(), name='thread-delete'),
    path('about/', views.about, name='forum-about'),
    re_path(r'^thread/(?P<object_id>\d+)/rate/(?P<score>[\d\-]+)$', GiveVote(), {
        'app_label': 'forum',
        'model': 'Thread',
        'field_name': 'rating',
    }, name="thread-rating"),
]