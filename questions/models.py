from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ProfileMod(models.Model):
    Provider_Name = models.CharField(max_length=1000)
    UserID = models.CharField(max_length=1000)
    Name = models.CharField(max_length=1000)
    Email = models.CharField(max_length=1000)
    Avatar = models.ImageField(null=True)
    Balance = models.FloatField(default=0)

    # Gender = models.CharField(max_length=10, null=True)
    # Date_of_birth = models.DateField(null=True)

    class Meta:
        db_table = 'ProfileMod'

    def __str__(self):
        return str(self.Name)


class QuestionSet(models.Model):
    QuestionName = models.CharField(max_length=1000)
    QuestionPrice = models.FloatField

    class Meta:
        db_table = 'QuestionSet'

    def __str__(self):
        return str(self.QuestionName)


class ChapterQuestion(models.Model):
    MVD = models.CharField(max_length=1)
    QuestionId = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    SubName = models.CharField(max_length=255)
    SubID = models.CharField(max_length=255)
    ChapterName = models.CharField(max_length=1000)
    Question = models.TextField(max_length=1000)
    Option1 = models.CharField(max_length=1000)
    Option2 = models.CharField(max_length=1000)
    Option3 = models.CharField(max_length=1000)
    Option4 = models.CharField(max_length=1000)
    CorrectAns = models.CharField(max_length=5)
    Equation = models.ImageField(null=True)

    class Meta:
        db_table = 'ChapterQuestion'

    def __str__(self):
        return str(self.SubName)


class ExQuestion(models.Model):
    MVD = models.CharField(max_length=1)
    QuestionId = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    Question = models.TextField(max_length=1000)
    Option1 = models.CharField(max_length=1000)
    Option2 = models.CharField(max_length=1000)
    Option3 = models.CharField(max_length=1000)
    Option4 = models.CharField(max_length=1000)
    CorrectAns = models.CharField(max_length=1000)
    Equation = models.ImageField(null=True)

    class Meta:
        db_table = 'ExQuestion'

    def __str__(self):
        return str(self.QuestionId)


class ExamHistory(models.Model):
    UserId = models.ForeignKey(ProfileMod, on_delete=models.CASCADE)
    UserName = models.CharField(max_length=500, null=True)
    QuestionId = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    QuestionName = models.CharField(max_length=10000, null=True)
    TableName = models.CharField(max_length=255)
    Marks = models.FloatField(null=True)
    Position = models.IntegerField(null=True)

    class Meta:
        db_table = 'ExamHistory'

    def __str__(self):
        return str(self.Marks)


class Board(models.Model):
    Notice = models.CharField(max_length=10000)
    Created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'Noticeboard'

    def __str__(self):
        return str(self.Notice)
