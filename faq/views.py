# faq/views.py
from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer

# GET API for listing FAQs
class FAQListAPIView(generics.ListAPIView):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'en')  # Language support
        return context

# POST API for creating FAQs
class FAQCreateAPIView(generics.CreateAPIView):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()