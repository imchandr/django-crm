from django.urls import path
from .views import (
    lead_create, lead_list, lead_details, lead_create,lead_update,lead_delete,
    LeadListView,LeadDetailsView, LeadCreateView,LeadUpdateView,LeadDeleteView

)
                    


app_name = "leads"
urlpatterns = [
    path('',LeadListView.as_view(), name='lead-list'),
    path('<int:pk>',LeadDetailsView.as_view(), name='lead-details'),
    path('create', LeadCreateView.as_view(), name='lead-create'),
    path('<int:pk>/update',LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete', LeadDeleteView.as_view(), name='lead-delete')
]
