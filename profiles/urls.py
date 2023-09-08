from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.ProfileUpdateView.as_view(), name='update'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='profiles/password.html'), name='password'),
    path('<str:username>/', views.ProfileDetailView.as_view(), name='detail'),
    path('<str:username>/follow/', views.ProfileFollowView.as_view(), name='follow')
]
