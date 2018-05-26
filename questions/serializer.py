from rest_framework import serializers
from .models import QuestionSet
from .models import ExMedicalQuestion
from .models import ExDentalQuestion
from .models import VarsityQuestion
from .models import ExVarsityQuestion
from .models import ChapterQuestion
from .models import ExamHistory


class QuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSet
        fields = '__all__'


class ExMedicalQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExMedicalQuestion
        fields = '__all__'


class ExDentalQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExDentalQuestion
        fields = '__all__'


class VarsityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarsityQuestion
        fields = '__all__'


class ExVarsityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExVarsityQuestion
        fields = '__all__'


class ChapterQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterQuestion
        fields = '__all__'


class ExamHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamHistory
        fields = '__all__'
