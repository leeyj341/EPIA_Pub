# epia의 urls

from django.urls import path
from . import views
app_name = "epia"

urlpatterns = [
    path("", views.index, name="index"),
    path("prepare/", views.prepare, name="prepare"),
    path("select_position/<int:company_pk>/", views.select_position, name="select_position"),
    path("select_question/<int:position_pk>/", views.select_question, name="select_question"),
    path("mypage_favorite/", views.mypage_favorite, name="mypage_favorite"),
    path("mypage_favorite/<int:favorite_pk>/delete/", views.mypage_favorite_delete, name="mypage_favorite_delete"),
    path("favorite_position/<int:company_pk>/", views.favorite_position, name="favorite_position"),
    path("favorite_question/<int:position_pk>/", views.favorite_question, name="favorite_question"),
    
    
    
   
    
]