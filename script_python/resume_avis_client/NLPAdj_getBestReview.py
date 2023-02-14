import spacy
from collections import Counter
from string import punctuation

import matplotlib.pyplot as plt
import numpy as np

from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline
# %% CONSTANTS

review0 = ("""
Excéllent, très professionnel, J'ai fais appelle a cette entreprise pour des travaux de plomberie et pour l'installation complète d'une douche le travail a été fait de manière très minutieuse malgré de nombreux imprévus qui sont arrivés. Cette entreprise a su bien réagir a chaque fois Je recommande vivement.
""", 5)
review1 =("""
Si vous cherchez quelqu'un de sérieux, professionnel et qui fait un travail au rendu remarquable vous avez trouvé votre artisan. Rajoutez à cela de très bon conseil,merci encore pour votre chantier
""", 5)
review2 =("""
J'ai eu affaire à cette entreprise pour de la démolition/désamiantage puis pour la rénovation intérieure totale d'un pavillon: Pour ce qui est de la démolition/désamiantage: je suis satisfait du travail fourni. Ca a été rapide et à un prix plus que compétitif (surtout pour le désamiantage d'un RDC de 67m2/ enlèvement de dalles amiantées. Par contre, pour ce qui est de la rénovation, c'est un désastre total: "malfaçons à tous les étages". Sans que ce soit exhaustif, voici quelques unes des "malfaçons": . Cloisons BA13 montées sans qu'elles soient d'aplomb et qui plus est non vissées sur le rail de sol (peut-être voulait t'il faire des économies de vis) . Aucune des portes posées au niveau de ces cloisons ne ferment correctement (je dois toutes les raboter) . Enduits à proprement parler "dégueulasse" et pour lesquel on m'a demandé une "rallonge" au niveau du prix alors qu'au final, pour ce qui est des plafonds: on voit les bandes sous la fine couche d'enduit et un peu partout la trace du couteau à lisser . Pour ce qui est de l'électricité: le tableau au ss-sol a été remplacé. il y a la barette de terre mais c'est tout: cette barette n'est reliée à aucun piquet de terre et la personne venue installer la Pompe à chaleur n'a pas arrêté de se prendre des coups de jus. J'ai dû moi-même enterrer un piquet de terre et le relier à une barette de mesure puis au tableau. Bref, pour ce qui est de la réno, c'est du travail "à l'économie", bâclé et peu soigneux 
""", 2)
listReview = [review0, review1, review2]

listeCompleteArtisanPositif = dict()
listeCompleteArtisanNegatif = dict()

# %% FUNCTIONS

nlp = spacy.load("fr_core_news_sm")
def get_hotwords(text):
    result = []
    pos_tag = ['ADJ'] 
    doc = nlp(text.lower()) 
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            # Utiliser lemma permet de mettre le mot sous sa forme originel (Complet => Complète)
            result.append(token.lemma_)
    return result

def askIfNeedToBeFrequent(adj) -> bool:
    fadj=open(r"listeAdjectif.txt",'a+', encoding='utf-8')
    fask=open(r"alreadyAsk.txt",'r+', encoding='utf-8')
    for line in fask :
        if adj.lower() in line.split(',') :
            fadj.close()
            return False
    fask.close()
    fask=open(r"alreadyAsk.txt",'a+', encoding='utf-8')
    isFrequent=input(f"Est-ce que {adj} doit être fréquent ? Oui / Non ")
    if isFrequent == "Non" :
        fask.write(adj.lower() + ',')
        fadj.close()
        fask.close()
        return False
    else :
        fadj.write(',' + adj.lower())
        fadj.close()
        fask.close()
        return True
    return False

def isAFrequentAdj(adj) -> bool:
    f=open(r"listeAdjectif.txt",'r', encoding='utf-8')
    l = []
    for line in f :
        for word in line.split(','):
            l.append(word.lower())
    f.close()
    if not adj.lower() in l :
        return askIfNeedToBeFrequent(adj)
    else : return True
        
def add_Occurence(listeReviewArtisan, word) :
    if word in listeReviewArtisan :
        listeReviewArtisan[word][0] += 1 
    else : 
        listeReviewArtisan[word] = [1, False]
    b = isAFrequentAdj(word)
    listeReviewArtisan[word][1] = b
        
def getTrueOccurence(listeReviewArtisan):
    for key in list(listeReviewArtisan) :
        if not listeReviewArtisan[key][1] : del listeReviewArtisan[key]
        else : listeReviewArtisan[key] = listeReviewArtisan[key][0]
        
def analyser_sentiment(phrase):
    tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine", use_fast=True)
    model = TFAutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine")
    pip = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
    result = pip(phrase)
    prediction = result[0]["label"]
    return prediction
# %% MAIN

for review, star in listReview :
    for sentence in review.split('.'):
        if analyser_sentiment(sentence) == 'POSITIVE':
            [add_Occurence(listeCompleteArtisanPositif, str(word)) for word in get_hotwords(sentence)]
        else :
            [add_Occurence(listeCompleteArtisanNegatif, str(word)) for word in get_hotwords(sentence)]

print(listeCompleteArtisanPositif)
print('\n')
print(listeCompleteArtisanNegatif)
    
getTrueOccurence(listeCompleteArtisanNegatif)
getTrueOccurence(listeCompleteArtisanPositif)

print('---')
print(listeCompleteArtisanPositif)
print('\n')
print(listeCompleteArtisanNegatif)

plt.style.use('_mpl-gallery')
x,y = zip(*list(listeCompleteArtisanPositif.items()))

# plot
fig, ax = plt.subplots()

ax.stem(y,x)

ax.set(xlim=(0,4))

plt.show()