from django.urls import path
from .views import CashMachineView, GetPDFView


urlpatterns = [
    path('cash_register/', CashMachineView.as_view(), name='register'),
    path('get_pdf/<str:file_name>/', GetPDFView.as_view(), name='get_pdf'),
]
