from django.urls import path

from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.PostFeedView.as_view(), name='index'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('new/', views.PostNewView.as_view(), name='new'),
]
