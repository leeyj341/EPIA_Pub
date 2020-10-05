from django.contrib import admin
from .models import Answer, Keyword


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'content', 'created_at']

class KeywordAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'word', 'count', 'wordtype']

# Register your models here.

admin.site.register(Answer, AnswerAdmin)
admin.site.register(Keyword, KeywordAdmin)