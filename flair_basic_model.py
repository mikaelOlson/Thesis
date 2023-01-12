from flair import embeddings
from flair.data import Corpus
from flair.data import Dictionary
from flair.datasets import ColumnCorpus
from flair.embeddings import BytePairEmbeddings, TransformerWordEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
import time
import torch
#Define columns
columns = {0: 'text', 1: 'ner'}
data_folder = '/home/ludvig/Thesis/data/randomized_data'
start = time.time()
corpus: Corpus = ColumnCorpus(data_folder, columns, train_file='train_small.txt', test_file='test_small.txt', dev_file='valid_small.txt',in_memory=True)
#corpus = corpus.downsample(0.001, downsample_test=True)
print(corpus)
print("Time to create Corpus: " + str(time.time()-start))

label_type = 'ner'

label_dict = Dictionary(add_unk=False)
label_dict.add_item('B-STREET')
label_dict.add_item('E-STREET')
label_dict.add_item('I-STREET')
label_dict.add_item('S-STREET')
label_dict.add_item('S-NUMBER')
label_dict.add_item('B-LEVEL')
label_dict.add_item('E-LEVEL')
label_dict.add_item('S-LEVEL')
label_dict.add_item('B-UNIT')
label_dict.add_item('E-UNIT')
label_dict.add_item('S-UNIT')
label_dict.add_item('S-POSTCODE')
label_dict.add_item('B-VEJBY')
label_dict.add_item('I-VEJBY')
label_dict.add_item('E-VEJBY')
label_dict.add_item('S-VEJBY')
label_dict.add_item('B-POSTNAVN')
label_dict.add_item('E-POSTNAVN')
label_dict.add_item('S-POSTNAVN')
label_dict.add_item('O')
#label_dict = corpus.make_label_dictionary(label_type=label_type)
#print(type(label_dict))
#label_dict.save('label_dict')
#input()
#embeddings = BytePairEmbeddings('da')
embeddings = TransformerWordEmbeddings('Maltehb/danish-bert-botxo')
#embedding_types = [FlairEmbeddings('multi-forward'),FlairEmbeddings('multi-backward')]
#embeddings = StackedEmbeddings(embeddings=embedding_types)
tagger = SequenceTagger(hidden_size=256,
                        tag_dictionary=label_dict,
                        tag_type=label_type,
                        use_crf=True, embeddings=embeddings)
                        

# 6. initialize trainer
trainer = ModelTrainer(tagger, corpus) #lägg till tensorboard

# 7. start training
trainer.train('resources/taggers/BERT',
              learning_rate=0.005,
              mini_batch_size=32,
              max_epochs=200, embeddings_storage_mode='cpu')
#Manually check test-data
