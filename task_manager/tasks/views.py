from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView 
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import UserLoginMixin, AuthorDeletionMixin
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm


# Create your views here.
class TasksListView(UserLoginMixin, FilterView):

    template_name = 'tasks/index.html'
    model = Task
    context_object_name = 'tasks'
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Show'),
    }
