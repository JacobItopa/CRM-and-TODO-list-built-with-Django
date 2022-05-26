from audioop import reverse
from unicodedata import category
from django.core.mail import send_mail
from multiprocessing import context
from re import template
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import lead, Agent, Category
from .forms import CustomUserCreationForm, LeadForm, LeadModelForm, AssingAgentForm, LeadCategoryUpdateForm
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agent.mixins import OrganisorAndLoginRequiredMixin

# Create your views here.
# CRUD+L = create, retrive, update, delete, list

class SignupView(generic.CreateView):
    template_name = "registration/signup.html" 
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

    

class LandingPageView(generic.TemplateView):
    template_name = 'landingpage.html'

def landing_page(request):
    return render(request, "landingpage.html")



class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leeds/lead_list.html" 
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = lead.objects.filter(organisation=user.userprofile, agent__isnull = False)
        else:
            queryset = lead.objects.filter(organisation=user.agent.organisation, agent__isnull = False)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset = lead.objects.filter(organisation=user.userprofile, agent__isnull = True)
            context.update({
                "unassigned_leads": queryset
            })
        return context

def lead_list(request):
    leads = lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, "leeds/lead_list.html", context)


class LeadDetailsView(LoginRequiredMixin, generic.DetailView):
    template_name = "leeds/lead_details.html" 
    context_object_name = 'Lead'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset


def lead_detail(request, pk):
    Lead = lead.objects.get(id=pk)
    context = {
        'Lead': Lead
    }
    return render(request, 'leeds/lead_details.html', context)




class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leeds/lead_create.html" 
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("lead_list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()

        send_mail(
            subject="A lead has been Created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=['test2@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)



def lead_create(request):
    form = LeadModelForm()
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leeds')
    context = {
        'form': form
    }
    return render(request, 'leeds/lead_create.html', context)



class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leeds/lead_update.html" 
    context_object_name = 'Lead'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("lead_list")

    def get_queryset(self):
        user = self.request.user
        return lead.objects.filter(organisation=user.userprofile)


def lead_update(request, pk):
    Lead = lead.objects.get(id=pk)
    form = LeadModelForm(instance=Lead)
    if request.method == 'POST':
        form = LeadModelForm(request.POST, instance=Lead)
        if form.is_valid():
            form.save()
            return redirect('/leeds')
    context = {
        'form':form,
        'Lead':Lead
    }
    return render(request, 'leeds/lead_update.html', context)



class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView): 
    queryset = lead.objects.all()
    template_name = "leeds/lead_delete.html"
    context_querey_name = 'Lead'

    def get_success_url(self):
        return reverse("lead_list")

    def get_queryset(self):
        user = self.request.user
        return lead.objects.filter(organisation=user.userprofile)

def lead_delete(request, pk):
    Lead = lead.objects.get(id=pk)
    Lead.delete()
    return redirect('/leeds')

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):

    template_name = "leeds/assign_agent.html"
    form_class = AssingAgentForm



    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("lead_list")

    def form_valid(self, form):
        agent = (form.cleaned_data['agent'])
        Lead = lead.objects.get(id = self.kwargs["pk"])
        Lead.agent = agent
        Lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leeds/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = lead.objects.filter(organisation=user.agent.organisation)
        context.update({
            "unassigned_lead_count":queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leeds/category_details.html"
    context_objects_name = "category"


    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        Lead = self.get_object().leads.all()
        context.update({
            "Lead":Lead
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leeds/lead_category_update.html" 
    context_object_name = 'Lead'
    form_class = LeadCategoryUpdateForm

    def get_success_url(self):
        return reverse("lead_detail", kwargs={"pk": self.get_object().id})

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset


#def lead_update(request, pk):
#    Lead = lead.objects.get(id=pk)
#    form = LeadForm()
#    if request.method == 'POST':
#        form = LeadForm(request.POST)
#        if form.is_valid():
#            first_name = form.cleaned_data['first_name']
#            last_name = form.cleaned_data['last_name']
#            age = form.cleaned_data['age']
#            Lead.first_name=first_name
#            Lead.last_name=last_name
#            Lead.age=age
#            Lead.save()
#            return redirect('/leeds')
#    context = {
#        'form':form,
#        'Lead':Lead
#    }
#    return render(request, 'leeds/lead_update.html', context)

#def lead_create(request):
#    form = LeadForm()
#    if request.method == 'POST':
#        form = LeadForm(request.POST)
#        if form.is_valid():
#            first_name = form.cleaned_data['first_name']
#            last_name = form.cleaned_data['last_name']
#            age = form.cleaned_data['age']
#            agent = Agent.objects.first()
#            lead.objects.create(
#                first_name=first_name,
#                last_name=last_name,
#                age=age,
#                agent=agent
#            )
#            return redirect('/leeds')
#    context = {
#        'form': form
#    }
#    return render(request, 'leeds/lead_create.html', context)