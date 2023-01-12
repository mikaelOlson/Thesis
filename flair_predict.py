from cProfile import label
from flair.data import Sentence
from flair.models import SequenceTagger
import flair
from numpy import TooHardError
import psycopg2
from seqeval.scheme import IOBES, Entities
import torch
from tqdm import tqdm
from collections import Counter

def fixTags(tokens, labels):
    #Carl Zahlmannsvej 7, 3400 Hillerød
    newTokens = []
    newLabels = []
    count = -1
    for i in range(len(tokens)):
        if(labels[i][0] == 'B' or labels[i][0] == 'S'):
            newTokens.append(tokens[i])
            if 'STREET' in labels[i]:
                newLabels.append('STREET')
            elif 'UNIT' in labels[i]:
                newLabels.append('UNIT')
            elif 'POSTNAVN' in labels[i]:
                newLabels.append('POSTNAVN')
            elif 'VEJBY' in labels[i]:
                newLabels.append('VEJBY')
            elif 'NUMBER' in labels[i]:
                newLabels.append('NUMBER')
            elif 'POSTCODE' in labels[i]:
                newLabels.append('POSTCODE')
            elif 'LEVEL' in labels[i]:
                newLabels.append('LEVEL')
            count+=1
        elif(labels[i][0] == 'I' or labels[i][0] == 'E'):
            newTokens[count]+=" " + tokens[i]
        
        #elif(labels[i][0] == 'S'):
    return newTokens, newLabels




def getLabels(tokens):
    labels = []
    for token in tokens:
        values = token.annotation_layers.values()  # token.annotation_layers.values() returns dict_values
        for [val] in values:  # val is of type flair Label - tuple with (tag, tag_probability)
            val = str(val)
            vals = val.split(' ')
            tag = vals[0]
            labels.append(tag)
    return labels

def IOBESFromPredict(pred):
    labels = []
    for k in pred: #'STREET','NUMBER','LEVEL','UNIT','VEJBY','POSTCODE,','POSTNAVN'
        if 'STREET' in k:
            print()
            
        elif 'NUMBER' in k:
            print()
        elif 'LEVEL' in k:
            print()
        elif 'UNIT' in k:
            print()
        elif 'VEJBY' in k:
            print()
        elif 'POSTCODE' in k:
            print()
        elif 'POSTNAVN' in k:
            print()
    return labels

def getIOBES(row):
    tags = []
    x = row[1].split()
    if(len(x) == 4):
        tags.append("B-STREET")
        tags.append("I-STREET")
        tags.append("I-STREET")
        tags.append("E-STREET")
    elif(len(x) == 5):
        tags.append("B-STREET")
        tags.append("I-STREET")
        tags.append("I-STREET")
        tags.append("I-STREET")
        tags.append("E-STREET")

    elif(len(x) == 3):
        tags.append("B-STREET")
        tags.append("I-STREET")
        tags.append("E-STREET")
    elif(len(x) == 2):
        tags.append("B-STREET")
        tags.append("E-STREET")
    else: 
        tags.append("S-STREET")

    tags.append("S-NUMBER")

    if(row[3] != 'null'):
        tags.append("S-LEVEL")
    if(row[4] != 'null'):
        x = row[4].split()
        if(len(x) == 2):
            tags.append("B-UNIT")
            tags.append("E-UNIT")
        else:
            tags.append("S-UNIT")

    if(row[5] != 'null'):
        x = row[5].split()
        if(len(x) == 3):
            tags.append("B-VEJBY")
            tags.append("I-VEJBY")
            tags.append("E-VEJBY")

        elif(len(x) == 4):
            tags.append("B-VEJBY")
            tags.append("I-VEJBY")
            tags.append("I-VEJBY")
            tags.append("E-VEJBY")

        elif(len(x) == 2):
            tags.append("B-VEJBY")
            tags.append("E-VEJBY")

        else: 
            tags.append("S-VEJBY")

    tags.append("S-POSTCODE")
    x = row[7].split()
    if(len(x) == 3):
        tags.append("B-POSTNAVN")
        tags.append("I-POSTNAVN")
        tags.append("E-POSTNAVN")
    elif(len(x) == 2):
        tags.append("B-POSTNAVN")
        tags.append("E-POSTNAVN")
    else: 
        tags.append("S-POSTNAVN")
            
    return tags
flair.device =  torch.device("cpu")
model = SequenceTagger.load("resources/taggers/BERT/best-model.pt")
conn = psycopg2.connect('host=localhost dbname=postgis user=postgres password=abc123')
curs = conn.cursor()
curs2 = conn.cursor()
sql = """SELECT address, street_name, house_number, floor, door, additional_city_name, 
             post_number, postnavn, ST_X(geog::geometry), ST_Y(geog::geometry) FROM test_small
             LIMIT 2"""
curs.execute(sql)
rows = curs.fetchall()
y_true = []
y_pred = []

for i in tqdm(range(len(rows))):
    row = rows[i]
    comparison = getIOBES(row)
    y_true.append(comparison)
    # betegnelse, gata, nr, floor, door, vejbynamn, pnr, postnavn
    x = row[8]
    y = row[9]
    #inputs = input('Address:   ')
    #inputs = 'Brolæggerstræde 12, 1450 København K'
    #coord = input('Coord (x y) from Google Maps:  ') #In wrong order for postgis so need to swap them
    #inputs = inputs.replace(',',' ')



    print('Connected to PostgreSQL!')
    print('Fetching all nearby addresses...')

    sql = """SELECT address, street_name, house_number, floor,
                    door, additional_city_name, post_number, postnavn,
                    ST_Distance(geog, ST_GeographyFromText('POINT({})')) AS dist
                    FROM addresses WHERE ST_DWithin(geog,ST_GeographyFromText('POINT({})'),1000 )
                    ORDER BY dist LIMIT 5""".format(str(x) + " " + str(y), str(x) + " " + str(y))
    curs.execute(sql)
    print('Success!')
    rows2 = curs.fetchall()

    print('predicting...')
    sentence = Sentence(row[0].replace(',',''))
    model.predict(sentence)
    tokens = []
    for t in sentence.tokens:
        tokens.append(t.text)
    labels = getLabels(sentence.tokens)
    print(tokens)
    print(labels)
    #tokens, labels = fixTags(tokens, labels)

    #labellist = ['STREET','NUMBER','LEVEL','UNIT','VEJBY','POSTCODE,','POSTNAVN']
    allLists = []
    print(list(rows2[0]))
    print(getIOBES(rows2[0]))
    #Systofte Bygade 33, Systofte, 4800 Nykøbing F
    for i in range(len(tokens)):
        l = []
        l.append(labels[i])
        for row in rows2: #allt context
            row = list(row)
            rowLabels = getIOBES(row)
            found = False
            for k in range(len(row)): #Gå genom varje beståndsdel av adress
                if (tokens[i] == str(row[k]) and not found):
                    l.append(labellist[k])
                    found = True
            
        allLists.append(l)

    finalLabels = []
    for l in allLists:
        c = Counter(l)
        finalLabels.append(c.most_common(1)[0][0])
    print(tokens)
    fixfinal =  '#FIXA TAGGARNA'
    print(fixfinal)


 

