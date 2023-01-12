import xlsxwriter
# Vejnamn = 6
# husnr = 7
# etage = 8
# dør = 9
# postnr = 11
#postnrnamn = 12

workbook = xlsxwriter.Workbook("parsed_data.xlsx")
worksheet = workbook.add_worksheet()
row = 0
column = 0
headlines = ["vejnamn", "husnr","etage","dor","postnr","postnrnavn"]
for item in headlines:
    worksheet.write(row, column, item)
    column +=1

row = 1
column = 0

f = open("xaa",'r')
file = f.readlines()
count = 1 #skip info line
for i in range(1, len(file)):
    line = file[i]
    x = line.split(',')
    worksheet.write(i, 0, x[6])
    worksheet.write(i, 1, x[7])
    worksheet.write(i,2,x[8])
    worksheet.write(i,3,x[9])
    worksheet.write(i,4,x[11])
    worksheet.write(i,5,x[12])
    #print("Number ", i)
    #print("Vejnamn: ", x[6], "\n")
    #print("husnr: ", x[7], "\n")
    #print("etage: ", x[8], "\n")
    #print("dor: ", x[9], "\n")
    #print("postnr: ", x[11], "\n")
    #print("postnrnavn: ", x[12], "\n")
    #print("---------------------------------")
f.close()
