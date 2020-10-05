# interview의 url
from django.urls import path
from . import views

app_name = 'interviews'

urlpatterns = [
    path("interview/", views.interview, name="interview"),
    path("interview_result/", views.interview_result, name="interview_result"),
    path("sort_word/",views.sort_word, name="sort_word"),
    path("keywordCall/", views.keywordCall, name="keywordCall"),
    path("save_audio/", views.save_audio, name="save_audio"),
    path("mypage_resultlist/", views.mypage_resultlist, name="mypage_resultlist"),
]