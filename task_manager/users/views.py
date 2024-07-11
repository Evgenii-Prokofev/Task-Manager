from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from task_manager.users.models import User
from task_manager.users.forms import UserCreateForm
from django.utils.translation import gettext_lazy as _


# Create your views here.
class UsersListView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):

    template_name = 'users/create.html'
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered')