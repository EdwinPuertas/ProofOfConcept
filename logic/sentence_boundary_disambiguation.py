import ast
import json
import os
import spacy
from random import choice, sample

nlp = spacy.load('es')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = ROOT_DIR + os.sep + 'data' + os.sep + 'input' + os.sep + 'chat_anonymo.json'

file = open(file_path, mode='r', encoding='utf-8')
data = json.loads(json.dumps(file.read()))
list_chat = ast.literal_eval(data)

rand_item = sample(list_chat, 10)

i = 0
for item in rand_item:
     if len(item['messages']) > 0:
         i = i + 1
         print('#### Chat # {0} ####'.format(i))
         print('Conversación {0}'.format(str(item['messages'])))
         print('Sentence Boundary Disambiguation chat # {}'.format(i))
         for stm in item['messages']:
             doc = nlp(stm)
             for span in doc.sents:
                 print("#> span:", span)

