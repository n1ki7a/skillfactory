from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from newsportal.models import Author
from sign.forms import ProfileEditForm


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'sign/profile_view.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class ProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ProfileEditForm
    model = User
    template_name = 'sign/profile_edit.html'
    success_url = reverse_lazy('profile_view')

    def get_object(self, queryset=None):
        return self.request.user


# Create your views here.
@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    if not Author.objects.filter(user=user).exists():
        Author.objects.create(user=user)
    return redirect(reverse_lazy('profile_view'))
