from django.forms.models import ModelForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView,CreateView,UpdateView,DeleteView

from leads.forms import LeadForm

from leads.models import User, Leads
from .forms import LeadForm, LeadModelForm

# class based views


class LandingPageView(TemplateView):
    template_name = 'landingpage.html'

def landing_page(request):
    return render(request, "landingpage.html")


class LeadListView(ListView):

    """
    defoulf context name in classbase views in object_list
    this way we can change the context name in the classbase views 
    """ 

    template_name = 'leads/lead_list.html'
    queryset = Leads.objects.all()
    context_object_name = 'leads' 

def lead_list(request):
    lead = Leads.objects.all()
    context = {
        "leads": lead
    }
    return render(request, "leads/lead_list.html", context) 


class LeadDetailsView(DetailView):
    template_name = 'leads/lead_details.html'
    queryset = Leads.objects.all()
    context_object_name = 'lead_info'         
    
def lead_details(request, pk):
    lead_details = Leads.objects.get(id=pk)
    context = {
        "lead_info": lead_details
    }
    return render(request, "leads/lead_details.html", context)


class LeadCreateView(CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')

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

class LeadUpdateView(UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Leads.objects.all()
    form_class = LeadModelForm
    context_object_name = 'lead_update'
    
    
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




class LeadDeleteView(DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Leads.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-list')

def lead_delete(request, pk):
    lead = Leads.objects.get(id=pk)
    context_object_name = 'lead'
    lead.delete()
    return redirect("/leads")   
        


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






