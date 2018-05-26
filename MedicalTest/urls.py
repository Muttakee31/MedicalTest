"""MedicalTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from questions import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('question/', views.QuestionSetList.as_view()),
    path('xdquestion/', views.ExDentalQuestionList.as_view()),
    path('xmquestion/', views.ExMedicalQuestionList.as_view()),
    path('xvquestion/', views.ExVarsityQuestionList.as_view()),
    path('vquestion/', views.VarsityQuestionList.as_view()),
    path('cquestion/', views.ChapterQuestionList.as_view()),
    path('ehistory/', views.ExamHistoryList.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
