from audioop import reverse
from django.shortcuts import render, redirect, reverse
from django.views import generic


from .models import task
from.forms import TaskModelForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('landing_page')
        return super(SignupView, self).get(*args, **kwargs)

class LandingPageView(generic.TemplateView):
    template_name = 'landingpage.html'

class TaskList(LoginRequiredMixin, generic.ListView):
    template_name = 'base/task_list.html'
    context_object_name = 'tasks'
    model = task 

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


class TaskDetail(LoginRequiredMixin, generic.DetailView):
    template_name = 'base/task_detail.html'
    context_object_name = 'task'
    model = task

class TaskCreate(LoginRequiredMixin, generic.CreateView):
    template_name = 'base/task_create.html'
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse("task")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, generic.UpdateView):
    template_name = 'base/task_update.html'
    form_class = TaskModelForm
    context_object_name = 'task'
    model = task

    def get_success_url(self):
        return reverse("task")

class TaskDelete(LoginRequiredMixin, generic.DeleteView):
    template_name = 'base/task_delete.html'
    context_onject_name = 'task'
    model = task

    def get_success_url(self):
        return reverse("task")



