from django.core.mail import send_mail
from django.forms.models import ModelForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, request
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView


from leads.models import Agent, Leads, Category
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm,AssignAgentForm

from agents.mixins import OrganisornAndLoginRequiredMixin

# class based views


class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('signup-sucess')

    def form_valid(self, form):
        # to send mail to
        send_mail(
            subject='Accounr Created Sucessfully',
            message='Thank you {{ form.cleaned_data[id_username]}} for creating new account in CRM ',
            from_email='admin@crm.com',
            recipient_list=['cksahuu@gmail.com']
        )

        return super(SignupView, self).form_valid(form)


class LandingPageView(TemplateView):
    template_name = 'landingpage.html'


class Signup_sucessView(TemplateView):
    template_name = 'signup_sucess.html'


def Signup_sucess(request):
    return render(request, "signup_sucess.html")


def landing_page(request):
    return render(request, "landingpage.html")


class LeadListView(LoginRequiredMixin, ListView):

    """
    defoulf context name in classbase views in object_list
    this way we can change the context name in the classbase views 
    """

    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user

        """inital queryset for organisation"""

        if user.is_organisor:
            queryset = Leads.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            '''filter for logedin agent'''
            queryset = Leads.objects.filter(
                organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user, agent__isnull=False)
        return queryset

    
    def get_context_data(self, **kwargs) :
        '''for un-assigned leads'''

        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Leads.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                'unassigned_leads': queryset
            })
        return context


def lead_list(request):
    lead = Leads.objects.all()
    context = {
        "leads": lead
    }
    return render(request, "leads/lead_list.html", context)


class LeadDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_details.html'
    context_object_name = 'lead_info'

    def get_queryset(self):
        user = self.request.user

        """inital queryset for irganisation"""

        if user.is_organisor:
            queryset = Leads.objects.filter(organisation=user.userprofile)
        else:
            '''filter for logedin agent'''
            queryset = Leads.objects.filter(
                organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset


def lead_details(request, pk):
    lead_details = Leads.objects.get(id=pk)
    context = {
        "lead_info": lead_details
    }
    return render(request, "leads/lead_details.html", context)


class LeadCreateView(OrganisornAndLoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        # to send mail to
        send_mail(
            subject='Lead Created Sucessfully',
            message='Thank you for creating new lead ',
            from_email='sarah_prkr@outlook.com',
            recipient_list=['cksahuu@gmail.com']
        )

        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        # print("receving a post request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/leads')
        # print("The lead has been created sucessfully")
    context = {
        "form": LeadModelForm()
    }
    return render(request, "leads/lead_create.html", context)


class LeadUpdateView(OrganisornAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm
    context_object_name = 'lead_update'

    def get_queryset(self):
        user = self.request.user

        """inital queryset for irganisation"""

        if user.is_organisor:
            queryset = Leads.objects.filter(organisation=user.userprofile)
            return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_update(request, pk):
    lead = Leads.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        'form': form,
        'lead': lead
    }

    return render(request, "leads/lead_update.html", context)


class LeadDeleteView(OrganisornAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user

        """inital queryset for irganisation"""

        if user.is_organisor:
            queryset = Leads.objects.filter(organisation=user.userprofile)
            return queryset

    def get_success_url(self):
        return reverse('leads:lead-list')


def lead_delete(request, pk):
    lead = Leads.objects.get(id=pk)
    context_object_name = 'lead'
    lead.delete()
    return redirect("/leads")

class AssignAgentView(OrganisornAndLoginRequiredMixin, FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update(
            {
                "request":self.request
            }
        )
        return kwargs


    def get_success_url(self):
        return reverse('leads:lead-list')


    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Leads.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin,ListView):
    template_name = 'leads/category_list.html'
    contxt_object_name = 'category_name'
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Leads.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Leads.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(Category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

# class CategoryDetailView(LoginRequiredMixin, DetailView):
#     template_name = 'leads/category_detail.html'
#     context_object_name = 'category'

    
#     def get_queryset(self):
#         user = self.request.user
#         # initial queryset of leads for the entire organisation
#         if user.is_organisor:
#             queryset = Category.objects.filter(
#                 organisation=user.userprofile
#             )
#         else:
#             queryset = Category.objects.filter(
#                 organisation=user.agent.organisation
#             )
#         return queryset


    
# def lead_update(request, pk):
#     lead = Leads.objects.get(id=pk)
#     form = LeadModelForm()
#     if request.method=="POST":
#         form = LeadModelForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save(lead)
#             return redirect("/leads")
#     context = {
#         "form":form,
#         "lead":lead
#     }

#     return render(request,"leads/lead_update.html", context)
