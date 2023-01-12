from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.data import Sentence
from flair.models import SequenceTagger
import time

s = Sentence('Warholms väg 8b 22465 Lund')
x = Sentence('Danskevej 23B 4800 Köbenhavn')
columns = {0: 'text', 1: 'ner'}
data_folder = '/home/ludvig/Thesis/Data/masked_data'
start = time.time()
corpus: Corpus = ColumnCorpus(data_folder, columns, train_file='train.txt', test_file='test.txt', dev_file='dev.txt',in_memory=True)
print('Corpus created.')
corpus = corpus.downsample(0.0001)
testdata = corpus.test
model = SequenceTagger.load("resources/taggers/sota-ner-flair/final-model.pt")
print(testdata)
model.evaluate(testdata,'B-STREET')
# for x in testdata:
#     print(x)
#     for a in x:
#         print(a.get_labels())
#         a.remove_labels()
        
#     print(x)
#     model.predict(x)
#     print(x)
#     input()