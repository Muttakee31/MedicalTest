from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import QuestionSet, ExDentalQuestion, ExMedicalQuestion, ExVarsityQuestion, VarsityQuestion, \
    ChapterQuestion, ExamHistory
# Create your views here.
from .serializer import QuestionSetSerializer, \
    ExDentalQuestionSerializer, ExMedicalQuestionSerializer, ExVarsityQuestionSerializer, \
    VarsityQuestionSerializer, ChapterQuestionSerializer, ExamHistorySerializer


class QuestionSetList(APIView):

    def get(self, request):
        questions = QuestionSet.objects.all()
        serializer = QuestionSetSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ExDentalQuestionList(APIView):

    def get(self, request):
        questions = ExDentalQuestion.objects.all()
        serializer = ExDentalQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ExMedicalQuestionList(APIView):

    def get(self, request):
        questions = ExMedicalQuestion.objects.all()
        serializer = ExMedicalQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ExVarsityQuestionList(APIView):

    def get(self, request):
        questions = ExVarsityQuestion.objects.all()
        serializer = ExVarsityQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class VarsityQuestionList(APIView):

    def get(self, request):
        questions = VarsityQuestion.objects.all()
        serializer = VarsityQuestionSerializer(questions, many=True)
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

    def get(self,request):
        questions = ExamHistory.objects.all()
        serializer = ExamHistorySerializer(questions, many=True)
        return Response(serializer.data)

    def post(self):
        pass
