# faq/admin.py
from django import forms
from django.contrib import admin  # Import the admin module
from .models import FAQ

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3}),
            'answer': forms.Textarea(attrs={'rows': 5}),
        }

@admin.register(FAQ)  # Now 'admin' is defined
class FAQAdmin(admin.ModelAdmin):
    form = FAQForm
    list_display = ['question', 'question_hi', 'question_bn', 'answer']
    search_fields = ['question', 'question_hi', 'question_bn']
    list_filter = ['question']