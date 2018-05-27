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
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from questions import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = {
    path('admin/', admin.site.urls),
    path('q_set/', views.QuestionSetList.as_view()),
    path('x_q/', views.ExQuestionList.as_view()),
    path('x_q/<year>/', views.get_ex_question_y),
    path('x_q/<year>/<mvd>/', views.get_ex_question_y_mvd),
    #   path('c_q/(?P<pk>[0-9]+)', views.get_chapter_question),
    #   url(r'^c_q/(?P<pk>[0-9]+)$', views.get_chapter_question),
    path('c_q/', views.ChapterQuestionList.as_view()),
    path('c_q/<sub>/', views.get_chapter),
    path('c_q/<sub>/<chapter>/', views.get_chapter_question),
    path('e_history/', views.ExamHistoryList.as_view()),
    path('e_history/<user_id>', views.get_history_user),

}

urlpatterns = format_suffix_patterns(urlpatterns)
