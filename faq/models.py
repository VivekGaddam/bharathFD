# faq/models.py
from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from googletrans import Translator
import logging

logger = logging.getLogger(__name__)

VALID_LANGUAGES = ['en', 'hi', 'bn']
CACHE_KEY_FORMAT = 'faq_{id}_question_{lang}'

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically translate questions if not provided
        if not self.question_hi or not self.question_bn:
            translator = Translator()
            try:
                if not self.question_hi:
                    self.question_hi = translator.translate(self.question, dest='hi').text
                if not self.question_bn:
                    self.question_bn = translator.translate(self.question, dest='bn').text
            except Exception as e:
                logger.error(f"Translation failed: {e}")
                # Fallback to English if translation fails
                self.question_hi = self.question_hi or self.question
                self.question_bn = self.question_bn or self.question
        super().save(*args, **kwargs)

    def get_translated_question(self, lang='en'):
        if lang not in VALID_LANGUAGES:
            raise ValueError(f"Invalid language code: {lang}")
        
        cache_key = CACHE_KEY_FORMAT.format(id=self.id, lang=lang)
        translated_question = cache.get(cache_key)
        
        if translated_question:
            logger.debug(f"Cache hit for key: {cache_key}")
            return translated_question
        
        logger.debug(f"Cache miss for key: {cache_key}")
        
        if lang == 'hi':
            translated_question = self.question_hi or self.question
        elif lang == 'bn':
            translated_question = self.question_bn or self.question
        else:
            translated_question = self.question
        
        cache.set(cache_key, translated_question, timeout=60 * 60)
        return translated_question