from postal.parser import parse_address
import psycopg2
import time
from tqdm import tqdm

def printError(parse, comparison, s):
    print("------------------------------------")
    print(parse)
    print("Correct: " + comparison)
    print("Libpostal: " + s)
    print("-------------------------------------")

start = time.time()
conn = psycopg2.connect('host=localhost dbname=postgis user=postgres password=abc123')
curs = conn.cursor()
sql = """ SELECT * FROM validationdata; """
curs.execute(sql)
correct_answers = 0
total_answers = 0
rows = curs.fetchall()
for i in tqdm(range(rows.__len__())):
    row = rows[i]
    total_answers = total_answers + 1
    parse = parse_address(row[0])
                # street,nr,floor,door,extra,postcode,postnavn
    c = [True,True,False,False,False,True, True]
    objects = ['road', 'house_number','level','unit','city','postcode','city']
    c[2] = row[3] != 'null'
    c[3] = row[4] != 'null'
    c[4] = row[5] != 'null'
    comparison = ""
    for i in range(7):
        if c[i]:
            comparison = comparison + objects[i] + ','
    s = ""
    for k in parse:
        s = s + k[1] + ","
    #printError(parse, comparison, s)
    if len(parse) < 7:
        if s == comparison:
            correct_answers = correct_answers + 1

            
print('Time run: ' + str(start - time.time()))
print("Total: ",total_answers," ","Correct: ",correct_answers)
print("Accuracy: ",correct_answers/total_answers,"%")
    
