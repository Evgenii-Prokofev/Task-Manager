from django import forms
from django.utils.translation import gettext as _

from task_manager.labels.models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _("Name")}),
        }
        labels = {
            'name': _("Name")
        }
