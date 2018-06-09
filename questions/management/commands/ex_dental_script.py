import xlrd
from django.core.management.base import BaseCommand, CommandError
from questions.models import ExQuestion, QuestionSet


class Command(BaseCommand):
    def handle(self, **options):
        # try:
        workbook = xlrd.open_workbook("C:\dantal-all.xlsx")
        worksheet_names = workbook.sheet_names()

        for i in range(len(worksheet_names)):
            sheet = workbook.sheet_by_name(worksheet_names[i])
            print(i)
            print("FML")
            for j in range(1, 101):
                qS = QuestionSet()
                cQ = ExQuestion()
                cQ.MVD = "D"
                print(sheet.cell(j, 1).value)
                cQ.Question = sheet.cell(j, 1).value
                if QuestionSet.objects.filter(Question=cQ.Question).exists():
                    continue
                print(cQ.Question)
                cQ.Option1 = sheet.cell(j, 2).value
                print(cQ.Option1)
                cQ.Option2 = sheet.cell(j, 3).value
                cQ.Option3 = sheet.cell(j, 4).value
                cQ.Option4 = sheet.cell(j, 5).value
                if QuestionSet.objects.filter(QuestionName=worksheet_names[i]).exists():
                    pass
                else:
                    qS = QuestionSet.objects.create(QuestionName=worksheet_names[i])
                    qS.QuestionPrice = 5
                qS = QuestionSet.objects.get(QuestionName=worksheet_names[i])
                cQ.QuestionId = qS
                cQ.CorrectAns = sheet.cell(j, 6).value

                cQ.save()
        # except Exception as e:
        #     CommandError(repr(e))
