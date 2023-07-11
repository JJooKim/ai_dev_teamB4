from django.db import models


# Create your models here.
class Youtube(models.Model):   
    def __str__(self): # 요게 뭐하는건지 확인
        return self.url
    url = models.URLField(default="Insert a Youtube Link", max_length=200, null = False)



    '''rf.
    문자열: CharField
    숫자: IntegerField, SmallIntegerField
    논리형 : BooleanField
    시간/날짜: DateTimeField
    '''