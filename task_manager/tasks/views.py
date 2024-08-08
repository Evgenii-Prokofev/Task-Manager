from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import UserLoginMixin, AuthorDeletionMixin
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filters import TaskFilter


# Create your views here.
class TasksListView(UserLoginMixin, FilterView):

    template_name = 'tasks/index.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Show'),
    }


class TaskDetailView(UserLoginMixin, DetailView):

    template_name = 'tasks/show.html'
    model = Task
    context_object_name = 'task'
    extra_context = {
        'title': _('Task preview')
    }


class TaskCreateView(UserLoginMixin, SuccessMessageMixin, CreateView):

    template_name = 'tasks/create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')
    extra_context = {
        'title': _('Create task'),
        'button_text': _('Create'),
    }

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TaskUpdateView(UserLoginMixin, SuccessMessageMixin, UpdateView):

    template_name = 'tasks/update.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully changed')
    extra_context = {
        'title': _('Task change'),
        'button_text': _('Change'),
    }


class TaskDeleteView(UserLoginMixin, AuthorDeletionMixin,
                     SuccessMessageMixin, DeleteView):

    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')
    author_message = _('The task can be deleted only by its author')
    author_url = reverse_lazy('tasks')
    extra_context = {
        'title': _('Delete task'),
        'button_text': _('Yes, delete'),
    }
