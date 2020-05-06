import spacy
nlp = spacy.load('es')
doc = nlp('Me gusta comer hamburguesa acompañada de vino en compañía de mis amigos y profesor')
for word in doc:
    print(word.text, word.tag_, word.pos_)


