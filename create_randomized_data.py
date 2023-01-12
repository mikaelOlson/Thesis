import psycopg2
import os
import random
from tqdm import tqdm


def print_context(row, file):
    x = row[1].split()
    

    if(len(x) == 4):
        file.write(x[0] + " O 1\n")
        file.write(x[1] + " O 1\n")
        file.write(x[2] + " O 1\n")
        file.write(x[3] + " O 1\n")
    elif(len(x) == 5):
        file.write(x[0] + " O 1\n")
        file.write(x[1] + " O 1\n")
        file.write(x[2] + " O 1\n")
        file.write(x[3] + " O 1\n")
        file.write(x[4] + " O 1\n")

    elif(len(x) == 3):
        file.write(x[0] + " O 1\n")
        file.write(x[1] + " O 1\n")
        file.write(x[2] + " O 1\n")
    elif(len(x) == 2):
        file.write(x[0] + " O 1\n")
        file.write(x[1] + " O 1\n")
    else:
        file.write(row[1] + " O 1\n")

    file.write(row[2] + " O 1\n")

    if(row[3] != 'null'):
        file.write(row[3] + ". O 1\n")
    if(row[4] != 'null'):
        x = row[4].split()
        if(len(x) == 2):
            file.write(x[0] + " O 1\n")
            file.write(x[1] + " O 1\n")
        else:
            file.write(row[4] + " O 1\n")

    if(row[5] != 'null'):
        x = row[5].split()
        if(len(x) == 3):
            file.write(x[0] + " O 1\n")
            file.write(x[1] + " O 1\n")
            file.write(x[2] + " O 1\n")

        elif(len(x) == 4):
            file.write(x[0] + " O 1\n")
            file.write(x[1] + " O 1\n")
            file.write(x[2] + " O 1\n")
            file.write(x[3] + " O 1\n")

        elif(len(x) == 2):
            file.write(x[0] + " O 1\n")
            file.write(x[1] + " O 1\n")

        else:
            file.write(row[5] + " O 1\n")

    file.write(str(row[6]) + " O 1\n")
    x = row[7].split()
    if(len(x) == 3):
        file.write(x[0] + " O 1\n")
        file.write(x[1] + " O 1\n")
        file.write(x[2] + " O 1\n")
    elif(len(x) == 2):
        file.write(x[0] + " O 1\n")
        file.write(x[1] + " O 1\n")
    else:
        file.write(row[7] + " O 1\n")


def create_dataset(path, table, useContext=False):
    if os.path.exists(path):
        os.remove(path)
    file = open(path, "w+")
    conn = psycopg2.connect(
        'host=localhost dbname=postgis user=postgres password=abc123')
    curs = conn.cursor()
    curs2 = conn.cursor()
    sql = """SELECT address, street_name, house_number, floor, door, additional_city_name, 
             post_number, postnavn, ST_X(geog::geometry), ST_Y(geog::geometry) FROM {}""".format(table)
    curs.execute(sql)
    rows = curs.fetchall()
    for i in tqdm(range(rows.__len__())):
        row = rows[i]
        # betegnelse, gata, nr, floor, door, vejbynamn, pnr, postnavn
        x = row[8]
        y = row[9]
        sql2 = """SELECT address, street_name, house_number, floor,
                door, additional_city_name, post_number, postnavn,
                ST_Distance(geog, ST_GeographyFromText('POINT({})')) AS dist
                FROM addresses WHERE ST_DWithin(geog,ST_GeographyFromText('POINT({})'),1000 )
                ORDER BY dist LIMIT 2""".format(str(x) + " " + str(y), str(x) + " " + str(y))
        

        row = list(row)
        row.pop(0)
        all_tokens = ['STREET', 'NUMBER', 'LEVEL', 'UNIT',
                      'vejbynamn', 'post_number', 'postnavn']
        dict_tokens = {}
        i = 0
        for token in all_tokens:
            dict_tokens[token] = i
            i += 1

        tokens = ['street_attr', 'vejbynamn', 'post_number', 'postnavn']

        random.shuffle(tokens)
        street_attr = ['STREET', 'NUMBER', ('LEVEL', 'UNIT')]
        random.shuffle(street_attr)

        new_street_attr = []
        for e in street_attr:
            if type(e) is tuple:

                new_street_attr.append(e[0])
                new_street_attr.append(e[1])
            else:
                new_street_attr.append(e)

        randomized_tokens_dict = {}
        for tok in tokens:
            if tok in dict_tokens:
                randomized_tokens_dict[tok] = dict_tokens[tok]
            else:
                for attr in new_street_attr:
                    randomized_tokens_dict[attr] = dict_tokens[attr]

        street = random.random()
        postcode = random.random()
        postnavn = random.random()

        if street < 0.5:
            for attr in new_street_attr:
                randomized_tokens_dict.pop(attr)

        if postcode < 0.5:
            randomized_tokens_dict.pop('post_number')
        if postnavn < 0.5:
            randomized_tokens_dict.pop('postnavn')

        for k, v in randomized_tokens_dict.items():

            if k == 'STREET':

                for attr in new_street_attr:
                    if attr == 'STREET':

                        x = row[v].split()
                        if(len(x) == 4):
                            file.write(x[0] + " B-STREET 0\n")
                            file.write(x[1] + " I-STREET 0\n")
                            file.write(x[2] + " I-STREET 0\n")
                            file.write(x[3] + " E-STREET 0\n")
                        elif(len(x) == 5):
                            file.write(x[0] + " B-STREET 0\n")
                            file.write(x[1] + " I-STREET 0\n")
                            file.write(x[2] + " I-STREET 0\n")
                            file.write(x[3] + " I-STREET 0\n")
                            file.write(x[4] + " E-STREET 0\n")

                        elif(len(x) == 3):
                            file.write(x[0] + " B-STREET 0\n")
                            file.write(x[1] + " I-STREET 0\n")
                            file.write(x[2] + " E-STREET 0\n")
                        elif(len(x) == 2):
                            file.write(x[0] + " B-STREET 0\n")
                            file.write(x[1] + " E-STREET 0\n")
                        else:
                            file.write(row[0] + " S-STREET 0\n")

                    elif attr == 'NUMBER':

                        file.write(row[1] + " S-NUMBER 0\n")

                    elif attr == 'LEVEL':

                        if(row[2] != 'null'):
                            file.write(row[2] + ". S-LEVEL 0\n")

                        if(row[3] != 'null'):
                            x = row[3].split()
                            if(len(x) == 2):
                                file.write(x[0] + " B-UNIT 0\n")
                                file.write(x[1] + " E-UNIT 0\n")
                            else:
                                file.write(row[3] + " S-UNIT 0\n")

            elif k == 'vejbynamn':
                x = row[v].split()

                if(row[4] != 'null'):
                    x = row[4].split()
                    if(len(x) == 3):
                        file.write(x[0] + " B-VEJBY 0\n")
                        file.write(x[1] + " I-VEJBY 0\n")
                        file.write(x[2] + " E-VEJBY 0\n")
                    elif(len(x) == 4):
                        file.write(x[0] + " B-VEJBY 0\n")
                        file.write(x[1] + " I-VEJBY 0\n")
                        file.write(x[2] + " I-VEJBY 0\n")
                        file.write(x[3] + " E-VEJBY 0\n")
                    elif(len(x) == 2):
                        file.write(x[0] + " B-VEJBY 0\n")
                        file.write(x[1] + " E-VEJBY 0\n")
                    else:
                        file.write(row[4] + " S-VEJBY 0\n")

            elif k == 'post_number':

                file.write(str(row[5]) + " S-POSTCODE 0\n")

            elif k == 'postnavn':

                x = row[6].split()
                if(len(x) == 3):
                    file.write(x[0] + " B-POSTNAVN 0\n")
                    file.write(x[1] + " I-POSTNAVN 0\n")
                    file.write(x[2] + " E-POSTNAVN 0\n")
                elif(len(x) == 2):
                    file.write(x[0] + " B-POSTNAVN 0\n")
                    file.write(x[1] + " E-POSTNAVN 0\n")
                else:
                    file.write(row[6] + " S-POSTNAVN 0\n")
        # This is where we print context
        if(useContext):
            curs2.execute(sql2)
            res = curs2.fetchall()
            context = res[1]
            print_context(context, file)
        file.write("\n")

    file.close()
    print("Created file {}".format(path))


create_dataset('data/randomized_data/test_small_context.txt', 'test_small', useContext=True)
create_dataset('data/randomized_data/train_small_context.txt', 'training_small', useContext=True)
create_dataset('data/randomized_data/valid_small_context.txt', 'valid_small', useContext=True)
