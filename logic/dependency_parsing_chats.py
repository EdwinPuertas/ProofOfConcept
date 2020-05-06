import ast
import json
import os
import spacy
import re
from random import choice, sample

def remplace_text(text):
    text = str(text)
    text = re.sub(r'ACT_([0-9]|[a-z])([a-z0-9]+)', 'NOMBRE', text)
    text = re.sub(r'NUM_([0-9]|[a-z])([a-z0-9]+)', 'NUMERO', text)
    text = re.sub(r'PHO_([0-9]|[a-z])([a-z0-9]+)', 'TELEFONO', text)
    text = re.sub(r'EML_([0-9]|[a-z])([a-z0-9]+)', 'EMAIL', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

nlp = spacy.load('es')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = ROOT_DIR + os.sep + 'data' + os.sep + 'input' + os.sep + 'chat_anonymo.json'

file = open(file_path, mode='r', encoding='utf-8')
data = json.loads(json.dumps(file.read()))
list_chat = ast.literal_eval(data)
# selecciona 10 registro de forma aleatoria
rand_item = sample(list_chat, 15)

i = 0
for item in rand_item:
    i = i + 1
    print('=' * 100)
    print('|' + (' '*45) + 'CHAT # '+str(i) + (' '*45)+'|')
    for stm in item['messages']:
        org_sentence = remplace_text(stm)
        print('=' * 100)
        print('|ORACIÓN ORIGINAL:')
        print('|' + str(org_sentence))
        doc = nlp(org_sentence)
        print('-' * 100)
        print('|{0:70}|{1:20}|{2:10}'.format('ORACIONES EXTRAIDAS', 'ROOT','POS'))
        print('-' * 100)
        for word in doc:
            dic_word = {}
            if word.pos_ in ('NOUN', 'VERB'):
                subtree_span = doc[word.left_edge.i: word.right_edge.i + 1]
                size = len(str(subtree_span).split(' '))
                if (size > 1 and size < 7):
                    print('|{0:70}|{1:20}|{2:10}'.format(subtree_span.text,subtree_span.root.text, subtree_span.root.pos_ ))
