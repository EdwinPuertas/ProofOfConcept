from textblob import TextBlob

blob = TextBlob("Me gusta comer hamburguesa acompañada de vino con la compañía de mis amigos y profesor")
print('Lenguaje detectado: ' + blob.detect_language())
print ('Word    |   POS')
print('=================')
for word, pos in blob.tags:
    print (word + " |   "+pos)