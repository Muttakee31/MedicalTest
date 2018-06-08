from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class QuestionSet(models.Model):
    QuestionName = models.CharField(max_length=40)
    QuestionPrice = models.IntegerField

    class Meta:
        db_table = 'QuestionSet'

    def __str__(self):
        return str(self.QuestionName)


class ChapterQuestion(models.Model):
    MVD = models.CharField(max_length=1)
    QuestionId = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    SubName = models.CharField(max_length=50)
    SubID = models.CharField(max_length=50)
    ChapterName = models.CharField(max_length=50)
    Question = models.TextField(max_length=1000)
    Option1 = models.CharField(max_length=50)
    Option2 = models.CharField(max_length=50)
    Option3 = models.CharField(max_length=50)
    Option4 = models.CharField(max_length=50)
    CorrectAns = models.CharField(max_length=1)
    Equation = models.ImageField(null=True)

    class Meta:
        db_table = 'ChapterQuestion'

    def __str__(self):
        return str(self.SubName)


class ExQuestion(models.Model):
    MVD = models.CharField(max_length=1)
    QuestionId = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    Question = models.TextField(max_length=1000)
    Option1 = models.CharField(max_length=50)
    Option2 = models.CharField(max_length=50)
    Option3 = models.CharField(max_length=50)
    Option4 = models.CharField(max_length=50)
    CorrectAns = models.CharField(max_length=1)
    Equation = models.ImageField(null=True)

    class Meta:
        db_table = 'ExQuestion'

    def __str__(self):
        return str(self.QuestionId)


class ExamHistory(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    QuestionId = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    TableName = models.CharField(max_length=15)
    Marks = models.FloatField(null=True)
    Position = models.IntegerField(null=True)

    class Meta:
        db_table = 'ExamHistory'

    def __str__(self):
        return str(self.marks)


class Board(models.Model):
    Notice = models.CharField(max_length=2000)
    Due_date = models.DateTimeField(null=True)
    Created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Noticeboard'

    def __str__(self):
        return str(self.notice)


class Profile(models.Model):
    IdToken = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    Name = models.TextField(max_length=1000)
    Email = models.CharField(max_length=50)
    Avatar = models.ImageField(null=True)
    Balance = models.IntegerField(default=0)
    Gender = models.CharField(max_length=5, null=True)
    Date_of_birth = models.DateField(null=True)

    class Meta:
        db_table = 'Profile'

    def __str__(self):
        return str(self.name)

#just_adding_random_comment