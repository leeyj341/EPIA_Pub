from django.db import models
from epia.models import Company, Position, Question
from django.conf import settings

# Create your models here.

DEFAULT_QUESTION_PK=1

# 면접 질문에 대한 답변 결과를 저장하는 테이블
class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.SET_DEFAULT,default=DEFAULT_QUESTION_PK)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"질문PK {self.question_id}, 유저PK {self.user_id} => {self.pk} : {self.content} : {self.created_at}"

# 답변에서 추출한 키워드
class Keyword(models.Model):
    answer = models.ForeignKey(to=Answer, on_delete=models.CASCADE)
    word = models.CharField(max_length=300)
    count = models.IntegerField()
    wordtype = models.IntegerField()

    def __str__(self):
        return f"답변PK {self.answer_id} => {self.pk} : {self.word} : {self.count} : {self.wordtype}"

# 면접자 사진 정보
def articles_image_path(instance, filename):
    return f'path/{filename}'

class Face(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    answer = models.ForeignKey(to=Answer, on_delete=models.CASCADE)
    path = models.CharField(max_length=500)
    image = models.ImageField(blank=True, upload_to=articles_image_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk} : 유저PK={self.user_id} : 답변PK={self.answer_id} : {self.path} : {self.created_at}"

