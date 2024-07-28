from django import forms

from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'cols': 0, 'rows': 0}),
        }
