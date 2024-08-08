from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, \
    UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import UserLoginMixin, DeleteProtectionMixin
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm


# Create your views here.
class LabelsListView(UserLoginMixin, ListView):

    template_name = 'labels/index.html'
    model = Label
    context_object_name = 'labels'
    extra_context = {
        'title': _('Labels'),
    }


class LabelsCreateView(UserLoginMixin, SuccessMessageMixin, CreateView):

    template_name = 'labels/create.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created')
    extra_context = {
        'title': _('Create label'),
        'button_text': _('Create'),
    }


class LabelsUpdateView(UserLoginMixin, SuccessMessageMixin, UpdateView):

    template_name = 'labels/update.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully changed')
    extra_context = {
        'title': _('Change label'),
        'button_text': _('Change'),
    }


class LabelsDeleteView(UserLoginMixin,
                       DeleteProtectionMixin,
                       SuccessMessageMixin,
                       DeleteView):

    template_name = 'labels/delete.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully deleted')
    protected_message = _('It is not possible to delete a label '
                          'because it is in use')
    protected_url = reverse_lazy('labels')
    extra_context = {
        'title': _('Delete label'),
        'button_text': _('Yes, delete'),
    }
