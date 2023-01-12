import json
import psycopg2
import os

def create_dataset(path, table):
    if os.path.exists(path):
        os.remove(path)
    file = open(path,"w+")
    conn = psycopg2.connect('host=localhost dbname=postgis user=postgres password=abc123')
    curs = conn.cursor()
    sql = """SELECT address, street_name, house_number, floor, door, additional_city_name,
            post_number, postnavn, geog, ST_X(geog::geometry), ST_Y(geog::geometry) FROM {}""".format(table)
    curs.execute(sql)
    #file.write('-DOCSTART- \n')
    for row in curs.fetchall():
    
    # IOBES tagging
    # I - Inside
    # O - Outside
    # B - Beginning
    # E - Ending
    # S - Single
    # betegnelse, gata, nr, floor, door, vejbynamn, pnr, postnavn
        x = row[1].split()
        #print(row[9])
        #input()

        if(len(x) == 4):
            file.write(x[0] + " B-STREET\n")
            file.write(x[1] + " I-STREET\n")
            file.write(x[2] + " I-STREET\n")
            file.write(x[3] + " E-STREET\n")
        elif(len(x) == 5):
            file.write(x[0] + " B-STREET\n")
            file.write(x[1] + " I-STREET\n")
            file.write(x[2] + " I-STREET\n")
            file.write(x[3] + " I-STREET\n")
            file.write(x[4] + " E-STREET\n")

        elif(len(x) == 3):
            file.write(x[0] + " B-STREET\n")
            file.write(x[1] + " I-STREET\n")
            file.write(x[2] + " E-STREET\n")
        elif(len(x) == 2):
            file.write(x[0] + " B-STREET\n")
            file.write(x[1] + " E-STREET\n")
        else: 
            file.write(row[1] + " S-STREET\n")

        file.write(row[2] + " S-NUMBER\n")

        if(row[3] != 'null'):
            file.write(row[3] + ". S-LEVEL\n")
        if(row[4] != 'null'):
            x = row[4].split()
            if(len(x) == 2):
                file.write(x[0] + " B-UNIT\n")
                file.write(x[1] + " E-UNIT\n")
            else:
                file.write(row[4] + " S-UNIT\n")

        if(row[5] != 'null'):
            x = row[5].split()
            if(len(x) == 3):
                file.write(x[0] + " B-VEJBY\n")
                file.write(x[1] + " I-VEJBY\n")
                file.write(x[2] + " E-VEJBY\n")

            elif(len(x) == 4):
                file.write(x[0] + " B-VEJBY\n")
                file.write(x[1] + " I-VEJBY\n")
                file.write(x[2] + " I-VEJBY\n")
                file.write(x[3] + " E-VEJBY\n")

            elif(len(x) == 2):
                file.write(x[0] + " B-VEJBY\n")
                file.write(x[1] + " E-VEJBY\n")

            else: 
                file.write(row[5] + " S-VEJBY\n")

        file.write(str(row[6]) + " S-POSTCODE\n")
        x = row[7].split()
        if(len(x) == 3):
            file.write(x[0] + " B-POSTNAVN\n")
            file.write(x[1] + " I-POSTNAVN\n")
            file.write(x[2] + " E-POSTNAVN\n")
        elif(len(x) == 2):
            file.write(x[0] + " B-POSTNAVN\n")
            file.write(x[1] + " E-POSTNAVN\n")
        else: 
            file.write(row[7] + " S-POSTNAVN\n")
        file.write("\n")
    file.close()
    print("Created file {}".format(path))

create_dataset('data/test_new.txt','testdata')
create_dataset('data/train_new.txt','trainingdata')
create_dataset('data/valid_new.txt','validationdata')
