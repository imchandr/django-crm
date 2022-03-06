from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class OrganisornAndLoginRequiredMixin(AccessMixin):
    '''verifies that current user is authrised and an organisor'''
    def dispatch(self,request,*args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect("leads:lead-list")
        return super().dispatch(request,*args,**kwargs)