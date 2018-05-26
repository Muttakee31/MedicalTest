from django.contrib import admin

from .models import QuestionSet
from .models import ChapterQuestion


# Register your models here.

admin.site.register(QuestionSet)
admin.site.register(ChapterQuestion)


