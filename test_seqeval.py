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
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



import time

from seqeval.scheme import IOBES, Entities
def flatten(t):
    return [item for sublist in t for item in sublist]

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


columns = {0: 'text', 1: 'ner'}
data_folder = '/home/ludvig/Thesis/data/randomized_data/'
start = time.time()
corpus: Corpus = ColumnCorpus(data_folder, columns,
                              train_file='train.txt',
                              test_file='test_small.txt',
                              dev_file='dev.txt',
                              in_memory=True)
print('Corpus created.')

y_true = []

testdata = corpus.test  # testdata = list of flair Sentence objects

for sent in testdata:

    tokens = sent.tokens  # tokens = list of flair Token objects

    y_true_sentence = []
    count = 0
    for token in tokens:

        values = token.annotation_layers.values()  # token.annotation_layers.values() returns dict_values
        
        for [val] in values:  # val is of type flair Label - tuple with (tag, tag_probability)
            val = str(val)
            vals = val.split(' ')
            tag = vals[0]
            y_true_sentence.append(tag)

    y_true.append(y_true_sentence)


model: SequenceTagger = SequenceTagger.load("resources/taggers/BPE.pt")
model.predict(testdata, return_loss=True, all_tag_prob=True, verbose=True)

y_pred = []

for sent in testdata:

    tokens = sent.tokens  # tokens = list of flair Token objects
    y_pred_sentence = []
    for token in tokens:
        values = token.annotation_layers.values()  # token.annotation_layers.values() returns dict_values

        for [val] in values:  # val is of type flair Label - tuple with (tag, tag_probability)
            val = str(val)
            vals = val.split(' ')
            tag = vals[0]
            y_pred_sentence.append(tag)

    y_pred.append(y_pred_sentence)

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



entities_true = Entities(y_true, IOBES, False)
entities_pred = Entities(y_pred, IOBES, False)
#y_true = [entity.tag for entity in chain(*entities_true.entities)]
#y_pred = [entity.tag for entity in chain(*entities_pred.entities)]
#print(len(y_pred) == len(y_true))


print("CLASSIFICATION REPORT: ", classification_report(corr_y_true, corr_y_pred, digits=5, mode='strict', scheme=IOBES))
print("F1 SCORE: ", f1_score(corr_y_true, corr_y_pred, mode='strict', scheme=IOBES))
print("ACCURACY SCORE: ", accuracy_score(corr_y_true, corr_y_pred))
print("PRECISION SCORE: ", precision_score(corr_y_true, corr_y_pred, mode='strict', scheme=IOBES))
print("RECALL SCORE: ", recall_score(corr_y_true, corr_y_pred, mode='strict', scheme=IOBES))

flat_true = flatten(y_true)
flat_pred = flatten(y_pred)
c_true = convert(flat_true)
c_pred = convert(flat_pred)
labels = ['LEVEL','NUMBER','POSTCODE','POSTNAVN','STREET','UNIT','VEJBY']
#matrix = confusion_matrix(flat_true,flat_pred,normalize=True,labels=['Level','Number','Postcode','Postnavn','Street','Unit','Vejby'])
matrix = confusion_matrix(c_true,c_pred,labels=labels)
matrix = matrix / matrix.astype(np.float).sum(axis=1)
print(matrix)
ax = sns.heatmap(matrix, annot=True, cmap='Blues', xticklabels=labels, yticklabels=labels, fmt='.3f')
fig = ax.get_figure()
#fig.savefig("BPE_confusion_matrix.png")
