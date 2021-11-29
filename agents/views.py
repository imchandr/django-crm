from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.forms.models import ModelForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from leads.models import Agent

from .forms import AgentModelForm
from .mixins import OrganisornAndLoginRequiredMixin
import random



# Agent list Views

class AgentListView(OrganisornAndLoginRequiredMixin,ListView):
    template_name ='agents/agent_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentDetailView(OrganisornAndLoginRequiredMixin,DetailView):
    template_name ='agents/agent_details.html'
    context_object_name = 'agents'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    

class AgentCreateView(OrganisornAndLoginRequiredMixin,CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"P{random.randint(0,1000)}")
        user.save()

        Agent.objects.create(
            user=user,
            
        )

        send_mail(
            subject="Leads CRM Agen acivation request",
            message="Your CRM agen id is genrated sucessfully please activate it through below link ",
            from_email="admin@crn.com",
            recipient_list = [user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentUpdateView(OrganisornAndLoginRequiredMixin,UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm
    context_object_name = 'agent_update'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    
    
    def get_success_url(self):
        return reverse("agents:agent-list")
    

class AgentDeleteView(OrganisornAndLoginRequiredMixin,DeleteView):
    
    template_name = 'leads/lead_delete.html'
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse('agents:agent-list')

    
