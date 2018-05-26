from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import QuestionSet, ExQuestion, ChapterQuestion, ExamHistory
# Create your views here.
from .serializer import QuestionSetSerializer, ExamHistorySerializer, ExQuestionSerializer, ChapterQuestionSerializer


class QuestionSetList(APIView):

    def get(self, request):
        questions = QuestionSet.objects.all()
        serializer = QuestionSetSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ExQuestionList(APIView):

    def get(self, request):
        questions = ExQuestion.objects.all()
        serializer = ExQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ChapterQuestionList(APIView):

    def get(self, request):
        questions = ChapterQuestion.objects.all()
        serializer = ChapterQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ExamHistoryList(APIView):

    def get(self, request):
        questions = ExamHistory.objects.all()
        serializer = ExamHistorySerializer(questions, many=True)
        return Response(serializer.data)

    def post(self):
        pass
