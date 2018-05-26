from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class QuestionSet(models.Model):
    QuestionName = models.CharField(max_length=40)
    QuestionPrice = models.IntegerField

    class Meta:
        db_table = 'QuestionSet'

    def __str__(self):
        return self.QuestionName


class ChapterQuestion(models.Model):
    MVD = models.IntegerField;
    SubName = models.CharField(max_length=50)
    SubID = models.CharField(max_length=50)
    ChapterName = models.CharField(max_length=50)
    Question = models.TextField(max_length=1000)
    Option1 = models.CharField(max_length=50)
    Option2 = models.CharField(max_length=50)
    Option3 = models.CharField(max_length=50)
    Option4 = models.CharField(max_length=50)
    CorrectAns = models.CharField(max_length=1)

    class Meta:
        db_table = 'ChapterQuestion'

    def __str__(self):
        return self.SubName


class ExQuestion(models.Model):
    MVD = models.IntegerField;
    QuestionId = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    Question = models.TextField(max_length=1000)
    Option1 = models.CharField(max_length=50)
    Option2 = models.CharField(max_length=50)
    Option3 = models.CharField(max_length=50)
    Option4 = models.CharField(max_length=50)
    CorrectAns = models.CharField(max_length=1)

    class Meta:
        db_table = 'ExQuestion'

    def __str__(self):
        return self.QuestionId


class ExamHistory(models.Model):
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Question_id = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    TableName = models.CharField(max_length=15)
    marks = models.IntegerField(null=True)
    position = models.IntegerField(null=True)

    class Meta:
        db_table = 'ExamHistory'

    def __str__(self):
        return self.marks
