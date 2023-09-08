from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import View, DetailView, TemplateView

from feed.models import Post
from followers.models import Follower
from .forms import UserUpdateForm, ProfileUpdateForm


class ProfileDetailView(DetailView):
    http_method_names = ['get']
    template_name = 'profiles/detail.html'
    model = User
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    request = None

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers'] = Follower.objects.filter(following=user).count()
        if self.request.user.is_authenticated:
            following = Follower.objects.filter(following=user, followed_by=self.request.user).exists()
            context['follow_text'] = 'Unfollow' if following else 'Follow'
            context['follow_action'] = 'unfollow' if following else 'follow'
        return context


class ProfileFollowView(LoginRequiredMixin, View):
    http_method_names = ['post']

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.POST.dict()

        if 'action' not in data or 'username' not in data:
            return HttpResponseBadRequest('Missing data.')

        try:
            following = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest(f"{data['username']} does not exist.")

        if data['action'] == 'follow':
            follower, created = Follower.objects.get_or_create(
                followed_by=request.user,
                following=following
            )
        else:
            try:
                follower = Follower.objects.get(
                    followed_by=request.user,
                    following=following
                )
            except Follower.DoesNotExist:
                follower = None

            if follower:
                follower.delete()

        return JsonResponse({
            'success': True,
            'wording': 'Unfollow' if data['action'] == 'follow' else 'Follow'
        })


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/update.html'
    request = None

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return redirect('profiles:update')
