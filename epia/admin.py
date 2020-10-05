from django.contrib import admin
from .models import Company, Position, Question, Ceo, Favorite

# Register your models here.
# 회사, 직무, 질문, 회장님 사진, 
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'name']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'position', 'content']

class CeoAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'path']

# 면접즐겨찾기 리스트
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'created_at']

admin.site.register(Company, CompanyAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Ceo, CeoAdmin)
admin.site.register(Favorite, FavoriteAdmin)
