from datetime import date

from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View, generic

from comments import forms as comment_forms
from comments import views as comment_views

from . import forms
from .models import Task


class TaskListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of all users tasks"""

    model = Task

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class ActiveTaskListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of users active tasks"""

    model = Task

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).filter(
            completed=False
        )


class CompletedTaskListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of users active tasks"""

    model = Task

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).filter(
            completed=True
        )


class TaskDetailView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    generic.detail.SingleObjectMixin,
    View,
):
    model = Task

    def get(self, request, *args, **kwargs):
        view = TaskDetailDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = comment_views.PostTaskComment.as_view()
        return view(request, *args, **kwargs)

    def test_func(self):
        task = self.get_object()
        return task.team_has_user(self.request.user)


class TaskDetailDisplay(generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = comment_forms.TaskCommentForm()
        return context


class TaskCreateView(
    mixins.LoginRequiredMixin, SuccessMessageMixin, generic.CreateView,
):
    model = Task
    form_class = forms.TaskForm
    success_message = "Task #%(id)s was created successfully"

    def get_initial(self):
        return {"assigned_to": self.request.user}

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = Task
    form_class = forms.TaskForm
    success_message = "Task #%(id)s was updated successfully"

    def get_initial(self):
        return {"assigned_to": self.request.user}

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        user = self.request.user

        if task.is_assigned_to(user):
            return True
        if task.is_team_leader(user):
            return True
        return False


class TaskCompleteView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = Task
    form_class = forms.CompleteTaskForm
    initial = {
        "date_completed": date.today(),
    }
    success_message = "Task #%(id)s completed"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.id,)

    def form_valid(self, form):
        form.instance.completed = True
        form.instance.completed_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        user = self.request.user

        if task.is_assigned_to(user):
            return True
        if task.is_team_leader(user):
            return True
        return False


class TaskDeleteView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView,
):
    model = Task
    success_url = "/tasks"

    def test_func(self):
        task = self.get_object()
        user = self.request.user

        return task.is_team_leader(user)
