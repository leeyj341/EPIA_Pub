from django.db import models
from django.conf import settings
# from epia.models import Question
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    birth = models.DateField()
    phone = models.CharField(max_length=40, unique=True)
    def __str__(self):
        return f"{self.username} : {self.password} : {self.first_name} : {self.last_name} : {self.birth} : {self.phone}"

# class Favorite(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
#     favorite_list = models.ManyToManyField(
#         settings.AUTH_USER_MODEL, related_name='favorite_list',
#         blank=True) # 게시글에 좋아요 없는 유효성 검사 통과할 수 있도록 blank=True 걸어준다.

    # def __str__(self):
    #     return f'{self.pk}번째 , {self.username}-{self.content}'