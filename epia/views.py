from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Position, Question, Favorite
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request, "epia/index.html")

# 면접 준비 페이지
# @login_required
def prepare(request):
    companies = Company.objects.exclude(pk=1)
    # paginator = Paginator(companies, 6)
    # page = request.GET.get('page')
    # companies = paginator.get_page(page)
    context = {
        "companies": companies
    }

    return render(request, "epia/prepare.html", context)

# 직무 선택
def select_position(request, company_pk):
    positions = Position.objects.filter(company_id=company_pk)
    context = {
        "positions": list(positions.values())
    }

    return JsonResponse(context)

# 질문 선택
def select_question(request, position_pk):
    questions = Question.objects.filter(position_id=position_pk)
    context = {
        "questions": list(questions.values())
    }

    return JsonResponse(context)

# 마이페이지 - 내 정보 보기
@login_required
def mypage_info(request):
    return render(request, "epia/mypage_info.html")

@login_required
def mypage_favorite_insert(request):
    return redirect('epia:mypage_favorite')

# 마이페이지 > 1) 질문 즐겨찾기 리스트 > [삭제] 기능
@login_required
@require_POST
def mypage_favorite_delete(request,favorite_pk):
    favorite = get_object_or_404(Favorite, pk=favorite_pk)
    favorite.delete()

    return redirect('epia:mypage_favorite')

#마이페이지 > 1) 질문 즐겨찾기 리스트 및 추가 페이지
@login_required
def mypage_favorite(request):
    if request.method == "POST":
        question = get_object_or_404(Question,pk=request.POST.get('question'))
        user=request.user
        if question in user.favorite_set.all():
            pass
        else:
            favorite = Favorite.objects.create(question_id=request.POST.get('question'),
                       question=request.POST.get('content'),
                       user=request.user,
                       created_at=request.POST.get('created_at'))
            favorite.save()
        return redirect('epia:mypage_favorite')
    else : 
        favorites = Favorite.objects.filter(user=request.user)
        companies = Company.objects.exclude(pk=1)
        context = {
            "companies": companies,
            'favorites' : favorites
        }

    return render(request, "epia/mypage_favorite.html", context)


# 직무 선택
def favorite_position(request, company_pk):
    positions = Position.objects.filter(company_id=company_pk)
    context = {
        "positions": list(positions.values())
    }

    return JsonResponse(context)

# 질문 선택
def favorite_question(request, position_pk):
    questions = Question.objects.filter(position_id=position_pk)
    context = {
        "questions": list(questions.values())
    }
    
    return JsonResponse(context)






