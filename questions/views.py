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
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import QuestionSet, ExQuestion, ChapterQuestion, ExamHistory, ProfileMod, Board
# Create your views here.
from .serializer import QuestionSetSerializer, ExamHistorySerializer, \
    ExQuestionSerializer, ChapterQuestionSerializer, ProfileModSerializer, BoardSerializer


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
        # qId = data['QuestionId']
        # uId = data['UserId']
        #        print(data['QuestionId'])
        #        print(data['UserId'])
        existent_user = ProfileMod.objects.get(UserID=data['UserId'])
        existent_question = QuestionSet.objects.get(id=int(data['QuestionId']))
        try:
            existent_res = ExamHistory.objects.get(QuestionId=data['QuestionId'], UserId=existent_user.id)
            existent_res.Marks = float(data['Marks'])
            existent_res.UserName = data['UserName']
            existent_res.save()
        except ObjectDoesNotExist:
            # ts = ExamHistory.objects.create(UserId=existent_user.id, QuestionId=int(data['QuestionId']))
            # ts.TableName=data['TableName']
            # ts.Marks=float(data['Marks'])
            ts = ExamHistory()
            ts.UserId = existent_user
            ts.QuestionId = existent_question
            ts.TableName = data['TableName']
            ts.Marks = float(data['Marks'])
            ts.save()
            ps = QuestionSet.objects.create(QuestionName="kheleche")
            return Response("done", status=status.HTTP_201_CREATED)
        return Response("notSaved", status=status.HTTP_201_CREATED)
        # return Response("NO User This Name", status=status.HTTP_400_BAD_REQUEST)


class ProfileModList(APIView):

    def get(self, request):
        questions = ProfileMod.objects.all()
        serializer = ProfileModSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        eId = data['Email']
        uId = data['UserID']
        # print(data['ProviderID'])
        # print(data['UserID'])

        existent_res = ProfileMod.objects.filter(UserID=uId, Email=eId)

        serializer = ProfileModSerializer(data=data)

        if serializer.is_valid():
            if existent_res:
                return Response("notSaved", status=status.HTTP_201_CREATED)
            else:
                ts = QuestionSet.objects.create(QuestionName=eId)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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
def get_id_question(request, qid):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        qset = QuestionSet.objects.get(id=qid)
        questions = ChapterQuestion.objects.filter(QuestionId=qset)
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
        qSet = QuestionSet.objects.get(QuestionName=year)
        questions = ExQuestion.objects.filter(QuestionId=qSet.id, MVD=mvd)
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
        qSet = QuestionSet.objects.get(QuestionName=year)
        questions = ExQuestion.objects.filter(QuestionId=qSet.id)
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
        q = ProfileMod.objects.get(UserID=user_id)
        # print(chapters)
        questions = ExamHistory.objects.filter(UserId=q)
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


@api_view(['GET', 'PUT', 'DELETE'])
def get_history_daily(request, exam_name):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        q = QuestionSet.objects.get(QuestionName=exam_name)
        # print(exam_name)
        # print(chapters)
        questions = ExamHistory.objects.filter(QuestionId=q)
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


@api_view(['GET', 'PUT', 'DELETE'])
def get_user(request, user_id):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        questions = ProfileMod.objects.get(UserID=user_id)
        # print(chapters)
        # questions = questionsquery.objects.get(ChapterName=chapter)
        # print(questions)
    except ProfileMod.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileModSerializer(questions)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # serializer = ExamHistorySerializer(questions, data=request.data)
        # if serializer.is_valid():
        #   serializer.save()
        #    return Response(serializer.data)
        return Response("no_put_here", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # questions.delete()
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
            # if userTrans:
            #     userTrans.Balance = userTrans.Balance + ssl_final['amount']
            #     userTrans.save()
            try:
                # ts = QuestionSet.objects.create(QuestionName=ssl_final['tran_id'])
                ts = QuestionSet.objects.create(QuestionName=ssl_final['amount'])
                userTrans = ProfileMod.objects.get(UserID=ssl_final['tran_id'])
                userTrans.Balance = userTrans.Balance + float(ssl_final['amount'])
                # ts = QuestionSet.objects.create(QuestionName=userTrans.Balance)
                userTrans.save()
            except ObjectDoesNotExist:
                pass

    return HttpResponse("fml")
