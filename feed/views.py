from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView

from .models import Post
from followers.models import Follower


class PostFeedView(TemplateView):
    http_method_names = ['get']
    template_name = 'feed/index.html'
    request = None

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all().order_by('-id')[0:30]
        if self.request.user.is_authenticated:
            following = list(Follower.objects.filter(followed_by=self.request.user).values_list('following', flat=True))
            if following:
                posts = Post.objects.filter(author__in=following).order_by('-id')[0:60]

        context['posts'] = posts
        return context


class PostDetailView(DetailView):
    http_method_names = ['get']
    template_name = 'feed/detail.html'
    model = Post
    context_object_name = 'post'


class PostNewView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'feed/create.html'
    fields = ['text']
    request = None
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        self.post = obj.save()
        return super(PostNewView, self).form_valid(form)
