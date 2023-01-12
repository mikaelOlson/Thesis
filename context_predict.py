import torch as torch
import numpy as np
import os
from torch import nn
import transformers
from accelerate import Accelerator
from huggingface_hub import Repository
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer

)
from ipywidgets import IntProgress
from tokenizers import decoders
from tokenizers.models import WordPiece
from tokenizers import Tokenizer
import psycopg2
from seqeval.scheme import IOBES, Entities
from tqdm import tqdm
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


model = AutoModelForTokenClassification.from_pretrained('/media/ludvig/ner')
tokenizer = AutoTokenizer.from_pretrained('Maltehb/danish-bert-botxo')


inputs = input('Address:   ')
coord = input('Coord (x y) from Google Maps:  ') #In wrong order for postgis so need to swap them
print('your input was: ' + inputs + ',' + coord)
inputs = inputs.replace(',',' ')
coord = coord.split(',')
y = coord[0]
x = coord[1]
print(x)
print(y)


conn = psycopg2.connect('host=localhost dbname=postgis user=postgres password=abc123')
curs = conn.cursor()
print('Connected to PostgreSQL!')
print('Fetching all nearby addresses...')

sql = """SELECT address, street_name, house_number, floor,
                door, additional_city_name, post_number, postnavn,
                ST_Distance(geog, ST_GeographyFromText('POINT({})')) AS dist
                FROM addresses WHERE ST_DWithin(geog,ST_GeographyFromText('POINT({})'),1000 )
                ORDER BY dist LIMIT 2""".format(str(x) + " " + str(y), str(x) + " " + str(y))
curs.execute(sql)
print('Success!')
rows = curs.fetchall()

print('predicting...')
data = tokenizer(inputs,rows[1][0], return_tensors="pt")

tokens = data.tokens()
outputs = model(**data).logits
predictions = torch.argmax(outputs, dim=2)

preds = []
for token, prediction in zip(tokens, predictions[0].numpy()):
    preds.append(model.config.id2label[prediction])
t, l = fix(tokens, preds)
res = ''
for i in range(len(t)):
    #print(t[i] + " " + l[i])
    res+=t[i] +  ' <' +l[i] + '>'
print(res)