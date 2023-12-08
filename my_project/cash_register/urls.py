from django.urls import path
from .views import CashMachineView


urlpatterns = [
    path('cash_register/', CashMachineView.as_view(), name='register'),
]
