from django.forms.models import ModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from leads.forms import LeadForm

from leads.models import Agent, Leads
from .forms import LeadForm, LeadModelForm


def lead_list(request):
    lead = Leads.objects.all()
    context = {
        "leads": lead
    }
    return render(request, "leads/lead_list.html", context)


def lead_details(request, pk):
    lead_details = Leads.objects.get(id=pk)
    context = {
        "lead_info": lead_details
    }
    return render(request, "leads/lead_details.html", context)


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
    return render(request, "leads/leads_create.html", context)

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

    return render(request, "leads/lead_update.html",context)

def lead_delete(request, pk):
    lead = Leads.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

    
    
