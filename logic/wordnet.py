import csv
import os
from nltk.corpus import wordnet

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
path_input = ROOT_DIR + os.sep + 'data' + os.sep + 'input' + os.sep + 'DiccionarioSinonimosUNESCO.csv'
path_output = ROOT_DIR + os.sep + 'data' + os.sep + 'output' + os.sep
list_synonyms = []
file = open(path_input, encoding='utf-8')
lines = csv.reader(file, dialect='excel', delimiter=';')
key = ''
value = ''
tuplas_synonym_UNESCO = []
# Crea la lista de los valores de
for item in lines:
    key = item[0].lower().strip().replace(' ','_')
    value = item[1].lower().strip().replace(' ','_')
    list_synonyms.append(key)
    list_synonyms.append(value)
    tuplas_synonym_UNESCO.append((key,value))

list_synonyms.pop(0)
list_synonyms.pop(0) # Elimina los titulos
tuplas_synonym_UNESCO.pop(0) # Elimina los titulos
d = {}
list_synonyms_clear = [d.setdefault(x, x) for x in list_synonyms if x not in d] # Elimina valores duplicados
list_synonyms_clear.pop()

dict_synonym = {}
dict_synonym_UNESCO = {}
for word in list_synonyms_clear:
    synonyms = []
    cont = 0
    for syn in wordnet.synsets(word, lang='spa'):
        for l in syn.lemmas(lang='spa'):
            synonyms.append(l.name().lower())
            cont +=1
            #if l.antonyms():
                #antonyms.append(l.antonyms()[0].name())
    if cont > 1:
        dict_synonym[word] = set(synonyms)
    else:
        list_tmp = []
        for i in tuplas_synonym_UNESCO:
            if word == i[0]:
                list_tmp.append(i[1])
        if len(list_tmp)>1:
            dict_synonym[word] = set(list_tmp)

list_synonyms_UNESCO_WORNET = []
for k,v in dict_synonym.items():
    for j in v:
        val = k.replace('_',' ') + ";" + j.replace('_',' ')
        list_synonyms_UNESCO_WORNET.append(val)
        print(val)

with open(path_output + 'DiccionarioSinonimosUNESC-WORDNET.csv', "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for value in list_synonyms_UNESCO_WORNET:
        writer.writerow([value])