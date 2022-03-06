from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView,

    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView,

    )
from django.urls import path, include
from leads.views import landing_page,Signup_sucessView, LandingPageView,SignupView



urlpatterns = [
    path('',LandingPageView.as_view(), name='landing-page'),
    path('admin/', admin.site.urls),

    #agents URL's
    path('agents/',include('agents.urls', namespace='agents-app')),

    # leads URL's
    path('leads/',include('leads.urls', namespace="leads-app")),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/sucess', Signup_sucessView.as_view(), name='signup-sucess'),

    #password-reset urls
    path('reset-password/',PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/',PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
