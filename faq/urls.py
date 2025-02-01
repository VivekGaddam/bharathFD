# faq/urls.py
from django.urls import path
from .views import FAQListAPIView, FAQCreateAPIView

urlpatterns = [
    path('api/faqs/', FAQListAPIView.as_view(), name='faq-list'),  # GET endpoint
    path('api/faqs/create/', FAQCreateAPIView.as_view(), name='faq-create'),  # POST endpoint
]