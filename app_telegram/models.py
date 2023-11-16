from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin

class TimeBasedModel(models.Model):
    class Meta:
        abstract = True
        ordering = ('-created',)

    created = models.DateTimeField(auto_now_add=True, verbose_name='Creted date')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated date')


class TGUser(TimeBasedModel):
    # Раскомментировать, если нужна связка с аккаунтами с сайта
    # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='пользователь')
    tg_id = models.BigIntegerField(unique=True, db_index=True, verbose_name='id Telegram')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.tg_id}'

#  universities
class University(models.Model):
    name = models.CharField(max_length=50)    
    fullname = models.CharField(max_length=150)  
    location = models.CharField(max_length=100, null=True)     
    
    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        return f'{self.name}'    
        
class Course(models.Model):
    name = models.CharField(max_length=50)    
    fullname = models.CharField(max_length=150)  
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f'{self.name}'

class CourseMessage(models.Model):
    name = models.CharField(max_length=50)    
    message = models.CharField(max_length=5000)  
    language = models.CharField(max_length=2)
    step = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Course message'
        verbose_name_plural = 'Course messages'

    def __str__(self):
        return f'{self.name}'
    
class Feedback(models.Model):
    name = models.CharField(max_length=50)
    message = models.CharField(max_length=5000)  
    language = models.CharField(max_length=2)
    step = models.IntegerField()
     
    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        return f'{self.name}'
    
class FeedbackData(models.Model):
    userid = models.IntegerField()
    username = models.CharField(max_length=50)
    language = models.CharField(max_length=2)
    clarity = models.CharField(max_length=50)
    clarity_comment = models.CharField(max_length=5000, null=True)
    usefulness = models.CharField(max_length=50)
    usefulness_comment = models.CharField(max_length=5000, null=True)
    support = models.CharField(max_length=50)
    support_comment = models.CharField(max_length=5000, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Feedback data'
        verbose_name_plural = 'Feedback datas'

    def __str__(self):
        return f'{self.userid}'