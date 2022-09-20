from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Application(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    introduction = models.TextField(null=False, max_length=300)     # 한 줄을 입력받는 CharField와 다르게 여러 줄을 입력받을 수 있음
    profile_image = models.ImageField(upload_to='uploads/%Y/%m/%d')
    nickname = models.CharField(null=False, max_length=10)
    job = models.CharField(null=False, max_length=100)

