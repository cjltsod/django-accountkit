from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('success', views.AccountKitSuccessView.as_view(), name='accountkit_success'),
]
