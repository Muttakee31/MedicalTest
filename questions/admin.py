from django.contrib import admin

from .models import QuestionSet
from .models import ExMedicalQuestion
from .models import ExDentalQuestion
from .models import VarsityQuestion
from .models import ExVarsityQuestion
from .models import ChapterQuestion


# Register your models here.

admin.site.register(QuestionSet)
admin.site.register(ExMedicalQuestion)
admin.site.register(ExDentalQuestion)
admin.site.register(VarsityQuestion)
admin.site.register(ChapterQuestion)
admin.site.register(ExVarsityQuestion)


