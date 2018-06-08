import xlrd

workbook = xlrd.open_workbook("C:\dantal-all.xlsx")
worksheet_names = workbook.sheet_names()

for i in range(len(worksheet_names)):
    sheet = workbook.sheet_by_name(worksheet_names[i])
    for j in range(1, 101):
        print(sheet.cell(j, 1).value)