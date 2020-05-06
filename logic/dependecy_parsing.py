import spacy
from spacy import displacy
from spacy.symbols import nsubj, VERB

text = "buenos días señor  Luis  X para nosotros es un agrado que visite nuestro servicio virtual, cuénteme ¿cómo ha estado el día de hoy?"

nlp = spacy.load('es')
doc = nlp(text)

print('|{0:15} |{1:8} |{2:8} |{3:15} |{4:8} |{5:20}'.format('TEXT', 'TEXT POS', 'DEP', 'HEAD TEXT', 'HEAD POS', 'CHILDREN'))
print('-' * 90)
options = {'compact': True, 'bg': '#ffffff',
           'color': '#000000', 'font': 'Arial', 'distance': 100}

for word in doc:
    print('|{0:15} |{1:8} |{2:8} |{3:15} |{4:8} |{5:20} '.format(word.text, word.pos_, word.dep_, word.head.text, word.head.pos_, str([child for child in word.children])))

print('Oraciones con dependencia')
for word in doc:

    if word.pos_ in ('NOUN', 'VERB', 'ADJ'):
        subtree_span = doc[word.left_edge.i : word.right_edge.i + 1]
        print(subtree_span.text, '|', subtree_span.root.text)

print('\n\nDependencias Izquierda y Derecha\n\n')

root = [token for token in doc if token.head == token][0]
subjectL = list(root.lefts)[0]
subjectR = list(root.rights)[0]
print('ROOT:{0}'.format(str(root)))
print('LEFTS:{0}'.format(list(root.lefts)))
print('RIGHTS:{0}'.format(list(root.rights)))
print('|{0:10} |{1:8} |{2:7} |{3:8} |{4:10}'.format('TEXT', 'DEP','N_LEFTS','N_RIGHTS', 'ANCESTORS'))
print('-'*90)
for descendant in subjectL.subtree:
     if subjectL is descendant or subjectL.is_ancestor(descendant):
         print('|{0:10} |{1:8} |{2:7} |{3:8} |{4:10}'.format(descendant.text, descendant.dep_, descendant.n_lefts, descendant.n_rights,
           str([ancestor.text for ancestor in descendant.ancestors])))


#spacy.displacy.serve(doc, style='dep', options=options)
