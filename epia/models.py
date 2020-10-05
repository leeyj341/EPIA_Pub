from django.db import models
from django.conf import settings

# Create your models here.


DEFAULT_COMPANY_PK=1
DEFAULT_POSITION_PK=1

# 회사 리스트
class Company(models.Model) :
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id} : {self.name}"

# 직무 리스트
class Position(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.SET_DEFAULT, default=DEFAULT_COMPANY_PK)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.company_id} => {self.id} : {self.name}"


# 각 회사의 면접 질문
class Question(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.SET_DEFAULT,default=DEFAULT_COMPANY_PK)
    position = models.ForeignKey(to=Position, on_delete=models.SET_DEFAULT,default=DEFAULT_POSITION_PK)
    content = models.TextField()

    def __str__(self):
        return f"{self.company_id}, {self.position_id} => {self.id} : {self.content}"

# 질문 즐겨찾기
class Favorite(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.question_id} => {self.id} : {self.created_at}"


# 회장님 사진 정보
class Ceo(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    mode = models.BooleanField()
    path = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.company_id} => {self.id} : {self.mode} : {self.path}"

