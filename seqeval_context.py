from itertools import chain
from flair.data import Corpus
from flair.datasets import ColumnCorpus, sequence_labeling
from flair.data import Sentence
from flair.models import SequenceTagger
from seqeval.metrics import accuracy_score
from seqeval.metrics import classification_report
from seqeval.metrics import f1_score
from seqeval.metrics import precision_score
from seqeval.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MultiLabelBinarizer
import matplotlib.pyplot as plt
import psycopg2
import numpy as np
import torch as torch
from tqdm import tqdm

from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer

)


import time

from seqeval.scheme import IOBES, Entities
def flatten(t):
    return [item for sublist in t for item in sublist]
def fix(a, b): #a = tokens, b = labels
    current = -1
    tokens = []
    labels = []
    for i in range(len(a)):
        if 'CLS' in a[i]:
            print('')
        elif 'SEP' in a[i]:
            break
        elif '#' in a[i]:
            temp = a[i].replace('#','')
            tokens[current]+=temp
            
        else:
            tokens.append(a[i])
            labels.append(b[i])
            current+=1
    return tokens, labels
def convert(t):
    a = []
    for k in t:
        if "STREET" in k:
            k = 'STREET'
            a.append('STREET')
        elif "NUMBER" in k:
            k = "NUMBER"
            a.append('NUMBER')
        elif "POSTCODE" in k:
            k = 'POSTCODE'
            a.append('POSTCODE')
        elif "POSTNAVN" in k:
            k = 'POSTNAVN'
            a.append('POSTNAVN')
        elif "LEVEL" in k:
            k = 'LEVEL'
            a.append('LEVEL')
        elif "UNIT" in k:
            k = 'UNIT'
            a.append('UNIT')
        elif "VEJBY" in k:
            k = 'VEJBY'
            a.append('VEJBY')
    return a
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele + ' '  
    
    # return string  
    return str1 

model = AutoModelForTokenClassification.from_pretrained('/media/ludvig/ner')
tokenizer = AutoTokenizer.from_pretrained('Maltehb/danish-bert-botxo')
print('model loaded')

conn = psycopg2.connect('host=localhost dbname=postgis user=postgres password=abc123')
curs = conn.cursor()
curs2 = conn.cursor()
sql = """SELECT address, street_name, house_number, floor, door, additional_city_name, 
             post_number, postnavn, ST_X(geog::geometry), ST_Y(geog::geometry) FROM test_small"""
curs.execute(sql)
rows = curs.fetchall()
y_true = []
y_pred = []
for i in tqdm(range(len(rows))):
    row = rows[i]
    # betegnelse, gata, nr, floor, door, vejbynamn, pnr, postnavn
    x = row[8]
    y = row[9]
    sql2 = """SELECT address, street_name, house_number, floor,
                door, additional_city_name, post_number, postnavn,
                ST_Distance(geog, ST_GeographyFromText('POINT({})')) AS dist
                FROM addresses WHERE ST_DWithin(geog,ST_GeographyFromText('POINT({})'),1000 )
                ORDER BY dist LIMIT 2""".format(str(x) + " " + str(y), str(x) + " " + str(y))
    curs2.execute(sql2)
    c = [True,True,False,False,False,True, True]
    objects = ['STREET', 'NUMBER','LEVEL','UNIT','VEJBY','POSTCODE','POSTNAVN']
    c[2] = row[3] != 'null'
    c[3] = row[4] != 'null'
    c[4] = row[5] != 'null'
    comparison = []
    for i in range(7):
        if c[i]:
            comparison.append(objects[i]) # y_true? 
    res = curs2.fetchall()
    context = res[1]
    y_true.append(comparison)
    address = row[0].replace(',',' ')
    data = tokenizer(address,res[1][0], return_tensors="pt")
    tokens = data.tokens()
    outputs = model(**data).logits
    predictions = torch.argmax(outputs, dim=2)

    preds = []
    for token, prediction in zip(tokens, predictions[0].numpy()):
        preds.append(model.config.id2label[prediction])
    t, l = fix(tokens, preds)
    y_pred.append(l)
    comp = ''
    for i in range(len(t)):
        #print(t[i] + " " + l[i])
        comp+=t[i] +  ' <' +l[i] + '>'
    #print('y_true: ' + listToString(comparison))
    #print('y_pred: ' + listToString(convert(l)))
    #print(comp)
    #print(row[0])#


mismatch_true = []
mismatch_pred = []
to_pop = []
corr_y_true = []
corr_y_pred = []

# Check if there are any differences in length 
# between true and predicted token arrays.
# Add those without differences to corr_y_true and corr_y_pred

for i in range(0,len(y_pred)):
    if len(y_pred[i]) != len(y_true[i]):

        mismatch_true.append(y_true[i])
        mismatch_pred.append(y_pred[i])
        to_pop.append(i)
    else:
        corr_y_true.append(y_true[i])
        corr_y_pred.append(y_pred[i])






print("CLASSIFICATION REPORT: ", classification_report(corr_y_true, corr_y_pred, digits=5, mode='strict', scheme=IOBES))
print("F1 SCORE: ", f1_score(corr_y_true, corr_y_pred, mode='strict', scheme=IOBES))
print("ACCURACY SCORE: ", accuracy_score(corr_y_true, corr_y_pred))
print("PRECISION SCORE: ", precision_score(corr_y_true, corr_y_pred, mode='strict', scheme=IOBES))
print("RECALL SCORE: ", recall_score(corr_y_true, corr_y_pred, mode='strict', scheme=IOBES))

