from django.urls import path
from . import views
from .views import adminCheck

urlpatterns = [
    path('register/', views.register, name='users-register'),
    path('profile/', views.profile, name='users-profile'),
    path('checkforadmin/', adminCheck, name='admin-check'),
]
