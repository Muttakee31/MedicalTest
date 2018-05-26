from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import QuestionSet, ExDentalQuestion, ExMedicalQuestion, ExVarsityQuestion, VarsityQuestion, ChapterQuestion, ExamHistory
# Create your views here.
from .serializer import QuestionSetSerializer


class QuestionSetList(APIView):

    def get(self,request):
        questions = QuestionSet.objects.all()
        serializer = QuestionSetSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self):
        pass
