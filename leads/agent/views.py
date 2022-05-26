import random as rd
from audioop import reverse
from random import random
from re import template
from urllib import request
from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leeds.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin

# Create your views here.
class AgentListView(OrganisorAndLoginRequiredMixin,generic.ListView):
    template_name = "agents/agent_list.html"
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agent_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{rd.randint(0, 10000)}")
        user.save()
        Agent.objects.create(
            user = user,
            organisation = self.request.user.userprofile,
            
        )
        #send_mail(
            #subject = "You're invited to be an agent",
            #message = "You were added as an agent on our CRM. please login to start working",
            #from_email = "admin@test.com",
            #recipient_list = [user.email]
        #)
        # agent.organisation = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_detail.html"
    context_object_name = 'agent'
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    contex_object_name = 'agent'

    def get_success_url(self):
        return reverse("agent_list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    contex_object_name = 'agent'

    def get_success_url(self):
        return reverse("agent_list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    



    


