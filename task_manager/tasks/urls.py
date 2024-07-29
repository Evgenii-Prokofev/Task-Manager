from django.urls import path
from task_manager.tasks import views


urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_show'),
    path('create/', views.TaskCreateView.as_view(), name='tasks_create'),
    path('<int:pk>/update/',
         views.TaskUpdateView.as_view(),
         name='tasks_update'),
    path('<int:pk>/delete/',
         views.TaskDeleteView.as_view(),
         name='tasks_delete'),
]
