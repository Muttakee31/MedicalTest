from rest_framework import serializers
from .models import QuestionSet
from .models import ExQuestion
from .models import ChapterQuestion
from .models import ExamHistory, ProfileMod, Board


class QuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSet
        fields = '__all__'


class ExQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExQuestion
        fields = '__all__'


class ChapterQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterQuestion
        fields = '__all__'


class ExamHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamHistory
        #    fields = '__all__'
        fields = ('UserId', 'QuestionId', 'TableName', 'marks', 'position')


class ProfileModSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileMod
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

