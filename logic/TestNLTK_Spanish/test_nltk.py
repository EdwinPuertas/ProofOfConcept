import re
from nltk import text
from nltk import bigrams
from nltk import trigrams
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
from nltk import word_tokenize
from nltk.text import Text
from nltk.probability import FreqDist
from util import Utils
from nltk.tokenize import sent_tokenize

class TNLTK:

    def __init__(self):
        self.util = Utils()
        self.newcorpus = ''
        self.list_stopwords =[]
        self.list_word = []
        self.token = []
        self.token_clean = []
        self.newcorpus_clean_token = ''
        self.newcorpus, self.list_word = self.util.get_corpus()
        self.stopwords = stopwords.words('spanish')

    def original_corpus(self):
        print('Corpus Sin Limpiar\n',self.newcorpus)
        self.token = word_tokenize(self.newcorpus,'spanish')
        print('Token Sin Limpiar\n',self.token)
        print('Token Stem Sin Limpiar\n',sent_tokenize(self.newcorpus))

    def clean_corpus(self):
        self.newcorpus_clean_token = self.util.clean_text(self.newcorpus)
        print('Corpus Limpio\n',self.newcorpus_clean_token)
        self.list_stopwords = self.stopwords
        self.token_clean = [i for i in self.newcorpus_clean_token if i not in self.list_stopwords]
        print('Tokens Limpio\n',self.token_clean)

    def metrics(self):
        fdist = FreqDist(self.token_clean)
        top_word = fdist.most_common(10)
        idx = text.ContextIndex(self.token)
        list_similarity = []
        for word in self.token:
            list_similarity.append(idx.similar_words(word))

        print('\nMetricas\n' +
                                '# Palabras Originales: ' + str(len(self.newcorpus)) + '\n' +
                                '# Palabras Limpias: ' + str(len(self.newcorpus_clean_token)) + '\n' +
                                'Dif Palabras: ' + str(len(self.token)-len(self.token_clean)) + '\n' +
                                'Concordance: ' + str(Text(self.token).concordance('sancho')) + '\n' +
                                'Similarity:', list_similarity ,
                                '\nSet de palabras: ', set(self.token),
                                '\nTop 10 Freq Plabras: ', top_word
        )

    def stopwords(self):
        return self.list_stopwords

    def stemmer(self):
        list_stm= []
        for stm in self.util.get_stemmer(self.token_clean):
           list_stm.append(stm)
        return list_stm

    def bigrams(self):
        return self.util.get_bigrams(self.newcorpus_clean_token)

    def pos_tag(self):
        return self.util.get_pos_tag(self.token_clean)

    def cal_tfidf(self):
        vocabulary = []
        ftokens = []
        docs = {}
        text, tokens_clean = self.util.read_text_file()

        tokens = RegexpTokenizer('[\w]+', flags = re.UNICODE).tokenize(text)
        bitokens = bigrams(tokens)
        tritokens = trigrams(tokens)

        tokens = [token.lower() for token in tokens if len(token)>0]
        tokens = [token for token in tokens if token not in self.stopwords]

        bitokens = [' '.join(token).lower() for token in bitokens]
        bitokens = [token for token in bitokens if token not in self.stopwords]

        tritokens = [' '.join(token).lower() for token in tritokens]
        tritokens = [token for token in tritokens if token not in self.stopwords]

        ftokens.extend(tokens)
        ftokens.extend(bitokens)
        ftokens.extend(tritokens)

        docs[text] = {'freq':{},'tf': {},'idf':{},'tf-idf':{}, 'tokens':[]}

        for token in ftokens:
            docs[text]['freq'][token] = self.util.freq(token, ftokens)
            docs[text]['tf'][token] = self.util.tf(token, ftokens)
            docs[text]['tokens'] = ftokens
            vocabulary.append(ftokens)

        for doc in docs:
            for token in docs[doc]['tf']:
                docs[doc]['idf'][token] = self.util.idf(token,vocabulary)
                docs[doc]['tf-idf'][token] = self.util.tfidf(token,docs[doc]['tokens'],vocabulary)

        words ={}
        for doc in docs:
            for token in docs[doc]['tf-idf']:
                if token not in words:
                    words[token] = docs[doc]['tf-idf'][token]
                else:
                    if docs[doc]['tf-idf'][token] > words[token]:
                        words[token] = docs[doc]['tf-idf'][token]
        for item in sorted(words.items(), key=lambda x:x[1], reverse=True):
            print('%f <= %s' % (item[1],item[0]))
