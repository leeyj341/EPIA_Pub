from django.shortcuts import render, redirect  
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, SignupForm ,UserPassChangeForm

# Create your views here.
# 로그인 페이지
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("epia:index")
    else:
        if request.user.is_authenticated :
            return redirect("epia:index")
        else :
            form = AuthenticationForm()
    context = {
        'form' : form
    }

    return render(request, "accounts/login.html", context)

#회원가입
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST) # 사용자가 POST방식으로 보내온 정보를 담아서 form 생성
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.birth = form.cleaned_data['birth']
            user.phone = form.cleaned_data['phone']
            user.save()
            auth_login(request, user)
            return redirect("accounts:login")
    else:
        form = SignupForm()
    context = {
        'form' : form
    }

    return render(request, 'accounts/form.html', context)

# 로그아웃
@login_required    
def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


# 마이페이지 - 내 정보/수정
@login_required
def mypage_info_update(request):
    if request.method =="POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.save()
            auth_login(request,user)
            return redirect("epia:index")
        else:
            print(form.errors)
    else:
        form =  CustomUserChangeForm(instance=request.user)
    context = {
        'form' : form
    }

    return render(request, "accounts/mypage_info.html")

@login_required
def password(request):
    if request.method == "POST":
        form = UserPassChangeForm(request.user, request.POST) # 순서 꼭 지키기
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:mypage_info_update')
    else:
        form = UserPassChangeForm(request.user)
    context = {
        'form' : form
    }
    
    return render(request, 'accounts/password.html', context)
