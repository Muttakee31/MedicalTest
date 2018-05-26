# Generated by Django 2.0.5 on 2018-05-26 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChapterQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SubName', models.CharField(max_length=50)),
                ('SubID', models.CharField(max_length=50)),
                ('CHapterNam', models.CharField(max_length=50)),
                ('Question', models.TextField(max_length=1000)),
                ('Option1', models.CharField(max_length=50)),
                ('Option2', models.CharField(max_length=50)),
                ('Option3', models.CharField(max_length=50)),
                ('Option4', models.CharField(max_length=50)),
                ('CorrectAns', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'ChapterQuestion',
            },
        ),
        migrations.CreateModel(
            name='ExDentalQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question', models.TextField(max_length=1000)),
                ('Option1', models.CharField(max_length=50)),
                ('Option2', models.CharField(max_length=50)),
                ('Option3', models.CharField(max_length=50)),
                ('Option4', models.CharField(max_length=50)),
                ('CorrectAns', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'ExDentalQuestion',
            },
        ),
        migrations.CreateModel(
            name='ExMedicalQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question', models.TextField(max_length=1000)),
                ('Option1', models.CharField(max_length=50)),
                ('Option2', models.CharField(max_length=50)),
                ('Option3', models.CharField(max_length=50)),
                ('Option4', models.CharField(max_length=50)),
                ('CorrectAns', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'ExMedicalQuestion',
            },
        ),
        migrations.CreateModel(
            name='ExVarsityQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question', models.TextField(max_length=1000)),
                ('Option1', models.CharField(max_length=50)),
                ('Option2', models.CharField(max_length=50)),
                ('Option3', models.CharField(max_length=50)),
                ('Option4', models.CharField(max_length=50)),
                ('CorrectAns', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'ExVarsityQuestion',
            },
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuestionName', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'QuestionSet',
            },
        ),
        migrations.CreateModel(
            name='VarsityQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SubName', models.CharField(max_length=50)),
                ('SubID', models.CharField(max_length=50)),
                ('CHapterNam', models.CharField(max_length=50)),
                ('Question', models.TextField(max_length=1000)),
                ('Option1', models.CharField(max_length=50)),
                ('Option2', models.CharField(max_length=50)),
                ('Option3', models.CharField(max_length=50)),
                ('Option4', models.CharField(max_length=50)),
                ('CorrectAns', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'VarsityQuestion',
            },
        ),
        migrations.AddField(
            model_name='exvarsityquestion',
            name='QuestionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.QuestionSet'),
        ),
        migrations.AddField(
            model_name='exmedicalquestion',
            name='QuestionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.QuestionSet'),
        ),
        migrations.AddField(
            model_name='exdentalquestion',
            name='QuestionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.QuestionSet'),
        ),
    ]
