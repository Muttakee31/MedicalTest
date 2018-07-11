from django.http import HttpResponse
from datetime import date, timedelta
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

        if data['QuestionId'] == 7070809 and data['Marks'] == 666:
            needed_balance = 900000
            try:
                superC = ExamHistory.objects.get(QuestionName=data['QuestionName'], UserId=existent_user.id)
                serializer = ExamHistorySerializer(superC)
                # ps = QuestionSet.objects.create(QuestionName="kheleche")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                if data['TableName'] == 'PMA':
                    superL = QuestionSet.objects.get(QuestionName='SUPERMED')
                    needed_balance = 100.0
                elif data['TableName'] == 'PVA':
                    superL = QuestionSet.objects.get(QuestionName='SUPERVAR')
                    needed_balance = 75.0
                available_money = existent_user.Balance
                if available_money - needed_balance > 0:
                    existent_user.Balance = available_money - needed_balance
                    existent_user.save()

                    ts = ExamHistory()
                    ts.UserId = existent_user
                    ts.UserName = existent_user.Name
                    ts.QuestionName = superL.QuestionName
                    ts.QuestionId = superL
                    ts.TableName = data['TableName']
                    ts.Marks = float(data['Marks'])
                    ts.save()
                    serializer = ExamHistorySerializer(ts)
                    # ps = QuestionSet.objects.create(QuestionName="kheleche")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                    # return Response("done", status=status.HTTP_201_CREATED)
                else:
                    return Response("not_done", status=status.HTTP_201_CREATED)

        else:
            existent_question = QuestionSet.objects.get(QuestionName=(data['QuestionName']))
        try:

            existent_res = ExamHistory.objects.get(QuestionId=existent_question.id, UserId=existent_user.id)
            existent_res.Marks = float(data['Marks'])
            existent_res.QuestionName = existent_question.QuestionName
            existent_res.QuestionId = existent_question
            existent_res.UserName = existent_user.Name
            existent_res.TableName = data['TableName']

            existent_res.save()
            serializer = ExamHistorySerializer(existent_res)
            # ps = QuestionSet.objects.create(QuestionName="kheleche")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            # ts = ExamHistory.objects.create(UserId=existent_user.id, QuestionId=int(data['QuestionId']))
            # ts.TableName=data['TableName']
            # ts.Marks=float(data['Marks'])
            ts = ExamHistory()
            ts.UserId = existent_user
            ts.UserName = existent_user.Name
            ts.QuestionId = existent_question
            ts.QuestionName = existent_question.QuestionName
            ts.TableName = data['TableName']
            ts.Marks = float(data['Marks'])
            available_money = existent_user.Balance

            try:
                superC = ExamHistory.objects.get(QuestionName='SUPERMED', UserId=existent_user.id)
                ts.save()
                serializer = ExamHistorySerializer(ts)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                try:
                    superD = ExamHistory.objects.get(QuestionName='SUPERVAR', UserId=existent_user.id)
                    ts.save()
                    serializer = ExamHistorySerializer(ts)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except ObjectDoesNotExist:
                    if available_money - 3.0 >= 0:
                        existent_user.Balance = available_money - 3.0
                        existent_user.save()
                        ts.save()
                        serializer = ExamHistorySerializer(ts)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response("notSaved", status=status.HTTP_201_CREATED)
            # ps = QuestionSet.objects.create(QuestionName="kheleche")
            return Response("notSaved", status=status.HTTP_201_CREATED)

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

                serializer.save()
                eh_user = ProfileMod.objects.get(UserID=uId)

                eh_que1 = QuestionSet.objects.get(id=29)
                # ts = QuestionSet.objects.create(QuestionName=eId)
                # serializer.save()
                eh_que2 = QuestionSet.objects.get(id=59)
                eh_que3 = QuestionSet.objects.get(id=71)
                eh_que4 = QuestionSet.objects.get(id=76)
                eh_que5 = QuestionSet.objects.get(id=81)
                eh_que6 = QuestionSet.objects.get(id=91)
                eh_que7 = QuestionSet.objects.get(id=106)
                eh_que8 = QuestionSet.objects.get(id=30)
                eh_table = 'C'

                eh1 = ExamHistory()
                eh1.TableName = eh_table
                eh1.UserId = eh_user
                eh1.QuestionId = eh_que1
                eh1.UserName = eh_user.Name
                eh1.QuestionName = eh_que1.QuestionName
                eh1.save()
                # ts = QuestionSet.objects.create(QuestionName=eId)
                eh2 = ExamHistory()
                eh2.TableName = eh_table
                eh2.UserId = eh_user
                eh2.QuestionId = eh_que2
                eh2.UserName = eh_user.Name
                eh2.QuestionName = eh_que2.QuestionName
                eh2.save()
                # ts = QuestionSet.objects.create(QuestionName=eId)
                eh3 = ExamHistory()
                eh3.TableName = eh_table
                eh3.UserId = eh_user
                eh3.QuestionId = eh_que3
                eh3.UserName = eh_user.Name
                eh3.QuestionName = eh_que3.QuestionName
                eh3.save()
                # ts = QuestionSet.objects.create(QuestionName=eId)
                eh4 = ExamHistory()
                eh4.TableName = eh_table
                eh4.UserId = eh_user
                eh4.QuestionId = eh_que4
                eh4.UserName = eh_user.Name
                eh4.QuestionName = eh_que4.QuestionName
                eh4.save()
                eh5 = ExamHistory()
                eh5.TableName = eh_table
                eh5.UserId = eh_user
                eh5.QuestionId = eh_que5
                eh5.UserName = eh_user.Name
                eh5.QuestionName = eh_que5.QuestionName
                eh5.save()
                eh6 = ExamHistory()
                eh6.TableName = eh_table
                eh6.UserId = eh_user
                eh6.QuestionId = eh_que6
                eh6.UserName = eh_user.Name
                eh6.QuestionName = eh_que6.QuestionName
                eh6.save()
                eh7 = ExamHistory()
                eh7.TableName = eh_table
                eh7.UserId = eh_user
                eh7.QuestionId = eh_que7
                eh7.UserName = eh_user.Name
                eh7.QuestionName = eh_que7.QuestionName
                eh7.save()
                eh8 = ExamHistory()
                eh8.TableName = eh_table
                eh8.UserId = eh_user
                eh8.QuestionId = eh_que8
                eh8.UserName = eh_user.Name
                eh8.QuestionName = eh_que8.QuestionName
                eh8.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardList(APIView):

    def get(self, request):
        questions = Board.objects.last()
        serializer = BoardSerializer(questions)
        return Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

        if 'daily' in sub:
            if 'DAILY EXAM 3' in chapter:
                if date.today() - date(2018, 7, 8) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 4' in chapter:
                if date.today() - date(2018, 7, 17) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 5' in chapter:
                if date.today() - date(2018, 7, 19) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 6' in chapter:
                if date.today() - date(2018, 7, 21) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 7' in chapter:
                if date.today() - date(2018, 7, 23) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 8' in chapter:
                if date.today() - date(2018, 7, 25) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 9' in chapter:
                if date.today() - date(2018, 7, 6) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 10' in chapter:
                if date.today() - date(2018, 7, 29) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 11' in chapter:
                if date.today() - date(2018, 7, 31) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 12' in chapter:
                if date.today() - date(2018, 8, 2) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 13' in chapter:
                if date.today() - date(2018, 8, 4) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 14' in chapter:
                if date.today() - date(2018, 8, 6) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 15' in chapter:
                if date.today() - date(2018, 8, 8) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 16' in chapter:
                if date.today() - date(2018, 8, 10) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 17' in chapter:
                if date.today() - date(2018, 8, 11) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 18' in chapter:
                if date.today() - date(2018, 8, 12) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 19' in chapter:
                if date.today() - date(2018, 8, 13) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 20' in chapter:
                if date.today() - date(2018, 8, 14) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 21' in chapter:
                if date.today() - date(2018, 8, 15) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 22' in chapter:
                if date.today() - date(2018, 8, 16) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 23' in chapter:
                if date.today() - date(2018, 8, 17) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 24' in chapter:
                if date.today() - date(2018, 8, 18) > timedelta(days=0):
                    return Response(serializer.data)

            elif 'DAILY EXAM 25' in chapter:
                if date.today() - date(2018, 8, 19) > timedelta(days=0):
                    return Response(serializer.data)
            elif 'DAILY EXAM 1' in chapter:
                if date.today() - date(2018, 7, 7) > timedelta(days=0):
                    return Response(serializer.data)
            elif 'DAILY EXAM 2' in chapter:
                if date.today() - date(2018, 7, 13) > timedelta(days=0):
                    return Response(serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND)

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

        chapter = qset.QuestionName

        if 'DAILY EXAM 3' in chapter:
            if date.today() - date(2018, 7, 8) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 4' in chapter:
            if date.today() - date(2018, 7, 18) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 5' in chapter:
            if date.today() - date(2018, 7, 20) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 6' in chapter:
            if date.today() - date(2018, 7, 22) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 7' in chapter:
            if date.today() - date(2018, 7, 24) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 8' in chapter:
            if date.today() - date(2018, 7, 26) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 9' in chapter:
            if date.today() - date(2018, 7, 6) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 10' in chapter:
            if date.today() - date(2018, 7, 30) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 11' in chapter:
            if date.today() - date(2018, 8, 1) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 12' in chapter:
            if date.today() - date(2018, 8, 3) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 13' in chapter:
            if date.today() - date(2018, 8, 5) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 14' in chapter:
            if date.today() - date(2018, 8, 7) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 15' in chapter:
            if date.today() - date(2018, 8, 9) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 16' in chapter:
            if date.today() - date(2018, 8, 11) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 17' in chapter:
            if date.today() - date(2018, 8, 12) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 18' in chapter:
            if date.today() - date(2018, 8, 13) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 19' in chapter:
            if date.today() - date(2018, 8, 14) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 20' in chapter:
            if date.today() - date(2018, 8, 15) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 21' in chapter:
            if date.today() - date(2018, 8, 16) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 22' in chapter:
            if date.today() - date(2018, 8, 17) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 23' in chapter:
            if date.today() - date(2018, 8, 18) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 24' in chapter:
            if date.today() - date(2018, 8, 19) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 25' in chapter:
            if date.today() - date(2018, 8, 20) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 1' in chapter:
            if date.today() - date(2018, 7, 7) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif 'DAILY EXAM 2' in chapter:
            if date.today() - date(2018, 7, 14) > timedelta(days=0):
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
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
    # store_id = "missiondmcadmissionaidlive"
    # store_passwd = "5B29E1782861136981"
    if request.method == 'POST':
        # qs = QuestionSet.objects.create(QuestionName=request.POST.get('verify_key'))
        # qs.QuestionPrice = 5
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
            # ts = QuestionSet.objects.create(QuestionName="wow")
            # ts.QuestionPrice = 5
            # url = 'https://securepay.sslcommerz.com/validator/api/validationserverAPI.php'
            url = 'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php'
            params = {'val_id': new_data['val_id'], 'store_id': store_id, 'store_passwd': store_passwd,
                      'format': "json"}
            r = requests.get(url, params=params)
            ssl_final = r.json()
            # ts = QuestionSet.objects.create(QuestionName=ssl_final['status'])
            # ts.QuestionPrice = 5
            # if userTrans:
            #     userTrans.Balance = userTrans.Balance + ssl_final['amount']
            #     userTrans.save()
            try:
                # ts = QuestionSet.objects.create(QuestionName=ssl_final['tran_id'])
                # ts = QuestionSet.objects.create(QuestionName=ssl_final['amount'])
                userTrans = ProfileMod.objects.get(UserID=ssl_final['tran_id'])
                userTrans.Balance = userTrans.Balance + float(ssl_final['amount'])
                # ts = QuestionSet.objects.create(QuestionName=userTrans.Balance)
                userTrans.save()
            except ObjectDoesNotExist:
                pass

    return HttpResponse("fml")