from django.contrib import admin

from .models import ChapterQuestion, QuestionSet, ExQuestion, ExamHistory, ProfileMod, Board


# Register your models here.

admin.site.register(QuestionSet)
admin.site.register(ChapterQuestion)
admin.site.register(ExQuestion)
admin.site.register(ExamHistory)
admin.site.register(ProfileMod)
admin.site.register(Board)
