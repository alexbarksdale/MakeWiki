from django.contrib import admin
from accounts.views import SignupView
from django.urls import path

urlpatterns = [
    # Signup
    path('signup/', SignupView.as_view(), name='signup')
]
