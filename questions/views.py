from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
import hashlib
from django.db.models import Q
from .models import QuestionSet, ExQuestion, ChapterQuestion, ExamHistory, Profile, Board
# Create your views here.
from .serializer import QuestionSetSerializer, ExamHistorySerializer, \
    ExQuestionSerializer, ChapterQuestionSerializer, ProfileSerializer, BoardSerializer


class QuestionSetList(APIView):

    def get(self, request):
        questions = QuestionSet.objects.all()
        serializer = QuestionSetSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExQuestionList(APIView):

    def get(self, request):
        questions = ExQuestion.objects.all()
        serializer = ExQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChapterQuestionList(APIView):

    def get(self, request):
        questions = ChapterQuestion.objects.all()
        serializer = ChapterQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChapterQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamHistoryList(APIView):

    def get(self, request):
        questions = ExamHistory.objects.all()
        serializer = ExamHistorySerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        qId = data['QuestionId']
        uId = data['UserId']
        print(data['QuestionId'])
        print(data['UserId'])

        existent_res = ExamHistory.objects.filter(QuestionId=qId, UserId=uId)

        serializer = ExamHistorySerializer(data=data)

        if serializer.is_valid():
            if not existent_res:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response("notSaved", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileList(APIView):

    def get(self, request):
        questions = Profile.objects.all()
        serializer = ProfileSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        qId = data['IdToken']
        uId = data['userId']
        print(data['IdToken'])
        print(data['userId'])

        existent_res = Profile.objects.filter(IdToken=qId, userId=uId)

        serializer = ProfileSerializer(data=data)

        if serializer.is_valid():
            if not existent_res:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response("notSaved", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardList(APIView):

    def get(self, request):
        questions = Board.objects.all()
        serializer = BoardSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass


@api_view(['GET', 'PUT', 'DELETE'])
def get_chapter_question(request, sub, chapter):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        questions = ChapterQuestion.objects.filter(SubName=sub, ChapterName=chapter)
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ChapterQuestion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChapterQuestionSerializer(questions, many=True)
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
        chapters = ChapterQuestion.objects.filter(SubName=sub)

        # chapters = chapters.objects.all()
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ChapterQuestion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChapterQuestionSerializer(chapters, many=True)
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
        questions = ExQuestion.objects.filter(QuestionId=year, MVD=mvd)
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ExQuestion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExQuestionSerializer(questions, many=True)
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
        questions = ExQuestion.objects.filter(QuestionId=year)
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ExQuestion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExQuestionSerializer(questions, many=True)
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
        questions = ExamHistory.objects.filter(UserId=user_id)
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ExamHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExamHistorySerializer(questions, many=True)
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


@require_POST
@csrf_exempt
def ipn_listener(request):
    store_id = "missi5b1bf9e7c190f"
    store_passwd = "missi5b1bf9e7c190f@ssl"
    if request.method == 'POST':
        qs = QuestionSet.objects.create(QuestionName=request.POST.get('verify_key'))
        qs.QuestionPrice = 5
        # qN=hashlib.md5("fml".endcode()).hexdigest()

        pre_define_key = request.POST.get('verify_key').split(',')

        new_data = {}
        if pre_define_key:
            for value in pre_define_key:
                if request.POST.get(value, -1) != -1:
                    new_data[value] = request.POST.get(value)

        new_data['store_passwd'] = hashlib.md5(store_passwd.encode()).hexdigest()

        hash_string = ''

        for key in sorted(new_data.keys()):
            hash_string += key + '=' + new_data[key] + '&'

        hash_string = hash_string.rstrip('&')

        #   rs = QuestionSet.objects.create(QuestionName="why")
        #   rs.QuestionPrice = 5

        if hashlib.md5(hash_string.encode()).hexdigest() == request.POST.get('verify_sign'):
            ts = QuestionSet.objects.create(QuestionName="wow")
            ts.QuestionPrice = 5
            url = 'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php'
            params = {'val_id': new_data['val_id'], 'store_id': store_id, 'store_passwd': store_passwd,
                      'format': "json"}
            r = requests.get(url, params=params)
            ssl_final = r.json()
            ts = QuestionSet.objects.create(QuestionName=ssl_final['status'])
            ts.QuestionPrice = 5

    return HttpResponse("fml")
