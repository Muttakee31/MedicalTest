# Generated by Django 2.0.5 on 2018-06-16 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Notice', models.CharField(max_length=10000)),
                ('Due_date', models.DateTimeField(null=True)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Noticeboard',
            },
        ),
        migrations.CreateModel(
            name='ChapterQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MVD', models.CharField(max_length=1)),
                ('SubName', models.CharField(max_length=255)),
                ('SubID', models.CharField(max_length=255)),
                ('ChapterName', models.CharField(max_length=1000)),
                ('Question', models.TextField(max_length=1000)),
                ('Option1', models.CharField(max_length=1000)),
                ('Option2', models.CharField(max_length=1000)),
                ('Option3', models.CharField(max_length=1000)),
                ('Option4', models.CharField(max_length=1000)),
                ('CorrectAns', models.CharField(max_length=5)),
                ('Equation', models.ImageField(null=True, upload_to='')),
            ],
            options={
                'db_table': 'ChapterQuestion',
            },
        ),
        migrations.CreateModel(
            name='ExamHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TableName', models.CharField(max_length=255)),
                ('Marks', models.FloatField(null=True)),
                ('Position', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'ExamHistory',
            },
        ),
        migrations.CreateModel(
            name='ExQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MVD', models.CharField(max_length=1)),
                ('Question', models.TextField(max_length=1000)),
                ('Option1', models.CharField(max_length=1000)),
                ('Option2', models.CharField(max_length=1000)),
                ('Option3', models.CharField(max_length=1000)),
                ('Option4', models.CharField(max_length=1000)),
                ('CorrectAns', models.CharField(max_length=1000)),
                ('Equation', models.ImageField(null=True, upload_to='')),
            ],
            options={
                'db_table': 'ExQuestion',
            },
        ),
        migrations.CreateModel(
            name='ProfileMod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Provider_Name', models.CharField(max_length=1000)),
                ('UserID', models.CharField(max_length=1000)),
                ('Name', models.CharField(max_length=1000)),
                ('Email', models.CharField(max_length=1000)),
                ('Avatar', models.ImageField(null=True, upload_to='')),
                ('Balance', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'ProfileMod',
            },
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QuestionName', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'QuestionSet',
            },
        ),
        migrations.AddField(
            model_name='exquestion',
            name='QuestionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.QuestionSet'),
        ),
        migrations.AddField(
            model_name='examhistory',
            name='QuestionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.QuestionSet'),
        ),
        migrations.AddField(
            model_name='examhistory',
            name='UserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.ProfileMod'),
        ),
        migrations.AddField(
            model_name='chapterquestion',
            name='QuestionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.QuestionSet'),
        ),
    ]
