from django.contrib import admin
from .models import Leads, Agent, User

admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Leads)

