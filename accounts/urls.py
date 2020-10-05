# accounts의 url
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/", views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path("mypage_info_update/",views.mypage_info_update, name="mypage_info_update"),
    path("password/", views.password, name="password"),

]