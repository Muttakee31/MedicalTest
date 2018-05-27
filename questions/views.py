from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
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


@api_view(['GET', 'PUT', 'DELETE'])
def get_chapter_question(request, sub, chapter):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        questions = ChapterQuestion.objects.get(SubName=sub, ChapterName=chapter)
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ChapterQuestion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChapterQuestionSerializer(questions)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ChapterQuestionSerializer(questions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        questions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def get_chapter(request, sub):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        chapters = ChapterQuestion.objects.get(SubName=sub)
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ChapterQuestion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChapterQuestionSerializer(chapters)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ChapterQuestionSerializer(chapters, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        chapters.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def get_ex_question_y_mvd(request, year, mvd):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        questions = ExQuestion.objects.get(QuestionId=year, MVD=mvd)
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ExQuestion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExQuestionSerializer(questions)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExQuestionSerializer(questions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        questions.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def get_ex_question_y(request, year):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        questions = ExQuestion.objects.get(QuestionId=year)
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ExQuestion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExQuestionSerializer(questions)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExQuestionSerializer(questions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        questions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def get_history_user(request, user_id):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        questions = ExamHistory.objects.get(UserId=user_id)
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ExamHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExamHistorySerializer(questions)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExamHistorySerializer(questions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        questions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)