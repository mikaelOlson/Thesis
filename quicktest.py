from flair.data import Sentence
from flair.models import SequenceTagger
import time
from postal.parser import parse_address


s = 'Lindingbrovej 2, Torstrup,Sig, 6800 Varde'
sentence = Sentence(s)
model = SequenceTagger.load("resources/taggers/zerofour/best-model.pt")
start = time.time()
print(parse_address(s))
print(time.time() - start)
start = time.time()
model.predict(sentence)
print(sentence)
print(time.time()-start)