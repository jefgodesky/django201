from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import Post


class PostFeedView(ListView):
    http_method_names = ['get']
    template_name = 'feed/index.html'
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-id')[0:30]


class PostDetailView(DetailView):
    http_method_names = ['get']
    template_name = 'feed/detail.html'
    model = Post
    context_object_name = 'post'


class PostNewView(CreateView):
    model = Post
    template_name = 'feed/create.html'
    fields = ['text']
