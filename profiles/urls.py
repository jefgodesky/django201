from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.ProfileUpdateView.as_view(), name='update'),
    path('<str:username>/', views.ProfileDetailView.as_view(), name='detail'),
    path('<str:username>/follow/', views.ProfileFollowView.as_view(), name='follow')
]
