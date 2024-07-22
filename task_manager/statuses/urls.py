from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='statuses'),
    path(
        'create/',
        views.StatusFormCreateView.as_view(),
        name='statuses_create'
    ),
    path(
        '<int:pk>/update/',
        views.StatusFormUpdateView.as_view(),
        name='statuses_update'
    ),
    path(
        '<int:pk>/delete/',
        views.StatusFormDeleteView.as_view(),
        name='statuses_delete'
    ),
]
