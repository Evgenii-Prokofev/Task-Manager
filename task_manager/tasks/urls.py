from django.urls import path
from task_manager.tasks import views


urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks'),
]
