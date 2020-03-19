from django.urls import path, re_path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from . import views

from updown.views import AddRatingFromModel


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    # path('post/<int:pk>/rate/<int:score>', AddRatingFromModel(), name="post-rating"), 
    re_path(r'^post/(?P<object_id>\d+)/rate/(?P<score>[\d\-]+)$', AddRatingFromModel(), {
        'app_label': 'blog',
        'model': 'Post',
        'field_name': 'rating',
    }, name="post-rating"),
]