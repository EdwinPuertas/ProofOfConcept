from logic.util import Utils
from logic.test_nltk import TNLTK

util = Utils()
test = TNLTK()
text, token = util.read_text_file()

print('Texto Original\n', text)
print('Texto Tokenizado\n', token)

test.original_corpus()
test.clean_corpus()

print('Stopword\n',test.stopwords)
print('Lista Stemmer\n', test.stemmer())
print('Lista Bigrams', test.bigrams())
print('Set Tag', test.pos_tag())
print(test.metrics())

print(test.cal_tfidf())

