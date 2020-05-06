import re
import os
import string
from math import log
from nltk import pos_tag
from nltk import bigrams
from nltk import word_tokenize
from nltk import ConditionalFreqDist
from nltk.corpus import PlaintextCorpusReader
from nltk.stem import SnowballStemmer

class Utils:

    def __init__(self):
        self.lang = 'spanish'
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.corpus_root = self.ROOT_DIR + '\corpus'
        self.path = self.ROOT_DIR + '\corpus\quijote1.txt'
        self.esp_stemmer = SnowballStemmer('spanish')
        self.corpus = PlaintextCorpusReader(self.corpus_root, '.*', encoding='utf-8')
        self.list_file_name = self.corpus.fileids()  # this gets name files of corpus

    def read_text_file(self):
        raw = open(self.path, 'r', encoding='utf-8')
        lines = raw.readlines()
        word_list = []
        text = ''
        for i in lines:
            text = text + i

        word_list = word_tokenize(text)
        return text, word_list

    def get_corpus(self):
        newcorpus = ''
        list_word = []
        for f in self.list_file_name:
            newcorpus = newcorpus + self.corpus.raw(f).lower()
            for word in self.corpus.words(f):
                list_word.append(word.lower())
        return newcorpus, list_word


    def clean_text(self, input):
        input = re.sub('\n+', " ", input)
        input = re.sub('\[[0-9]*\]', "", input)
        input = re.sub(' +', " ", input)
        input = re.sub('\((.*?)\)', " ", input)
        input = bytes(input, "UTF-8")
        input = input.decode("ascii", "ignore")
        cleanInput = []
        input = input.split(' ')
        for item in input:
            item = item.strip(string.punctuation)
            if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
                cleanInput.append(item)
        return cleanInput

    def get_stemmer(self, list_word):
        list = []
        for w in list_word:
            list.append(self.esp_stemmer.stem(w))

        d = {}
        # Elimina los elemntos duplicados
        list = [d.setdefault(x, x) for x in list if x not in d]
        return list

    def get_bigrams(self, text):
        list_bigrams = bigrams(text)
        cfd = ConditionalFreqDist(list_bigrams)
        list =[]
        for i in cfd:
            list.append(cfd[i])
        return list

    def get_pos_tag(self, token):
        list_tag = set(pos_tag(token, lang='esp'))
        list = [t for t in list_tag if (t[1] == "NN" or t[1] == "NNP" or t[1] == "VB" or t[1] == "VBZ")]
        return list

    def freq(self,word, doc):
        return doc.count(word)

    def word_count(self,doc):
        return len(doc)

    def tf(self, word, doc):
        den = 1.0
        if float(self.word_count(doc)) > 0.0:
            den = float(self.word_count(doc))
        val = self.freq(word, doc) / den
        return val

    def docs_contains(self, word, doc_list):
        count = 0
        for document in doc_list:
            if self.freq(word,document) > 0 :
                count += 1
        return (1 + count)

    def idf(self, word, doc_list):
        val = log(len(doc_list)/ float(self.docs_contains(word,doc_list)))
        return val

    def tfidf(self, word, doc, doc_list):
        val = self.tf(word, doc) * self.idf(word, doc_list)
        return val
