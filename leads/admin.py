from django.contrib import admin
from .models import Leads, Agent, User, UserProfile, Category

admin.site.register(UserProfile)
admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Leads)
admin.site.register(Category)

