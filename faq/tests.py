# faq/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import FAQ

class FAQAPITest(APITestCase):
    def test_fetch_faqs(self):
        FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework.",
            question_hi="डीजेंगो क्या है?",
            question_bn="ডjango কি?"
        )
        
        url = reverse('faq-list') 
        response = self.client.get(url, {'lang': 'hi'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "डीजेंगो क्या है?")