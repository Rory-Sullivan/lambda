from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="tasks"),
    path("create/", views.TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path(
        "task/<int:pk>/delete",
        views.TaskDeleteView.as_view(),
        name="task-delete",
    ),
]
