from flair.data import Corpus
from flair.datasets import ColumnCorpus, sequence_labeling
from flair.data import Sentence
from flair.models import SequenceTagger
# from seqeval.metrics import accuracy_score
# from seqeval.metrics import classification_report
# from seqeval.metrics import f1_score
# from flair.training_utils import Result
import time


columns = {0: 'text', 1: 'ner'}
data_folder = '/home/mikael/Thesis/repo/Thesis/small/small_data'
start = time.time()
corpus: Corpus = ColumnCorpus(data_folder, columns,
                              train_file='small_train.txt',
                              test_file='small_test.txt',
                              dev_file='small_dev.txt',
                              in_memory=True)
print('Corpus created.')


corpus = corpus.downsample(0.7)

y_true = []


testdata = corpus.test  # testdata = list of flair Sentence objects
print(len(testdata))
for x in testdata:
    sentence: Sentence = x
    tokens = sentence.tokens  # tokens = list of flair Token objects

    # print("----------------------------------------------------")
    # print("----------------------------------------------------")
    # print("\n")
    # print("SENTENCE: ", sentence)
    # print(("\n"))
    # print("TOKENS: ", tokens)
    y_true_sentence = []
    for token in tokens:
        values = token.annotation_layers.values()  # token.annotation_layers.values() returns dict_values

        for [val] in values:  # val is of type flair Label - tuple with (tag, tag_probability)
            # print(val)
            val = str(val)
            vals = val.split(' ')
            tag = vals[0]
            # print("\n")
            # print("TAG: ", tag)
            y_true_sentence.append(tag)

    y_true.append(y_true_sentence)
    # print("TRUE TAGS: ", y_true_sentence)
    # print("\n")
    # print("----------------------------------------------------")
    # print("----------------------------------------------------")
    # print("\n")
print("LENGTH OF TRUE TAGS: ", len(y_true))

# print("FINAL TRUE TAGS: ", y_true)
model: SequenceTagger = SequenceTagger.load("small/resources/taggers/sota-ner-flair/final-model.pt")

pred = model.predict(testdata, return_loss=True, all_tag_prob=True, verbose=True)

print(pred[:20])
y_pred = []