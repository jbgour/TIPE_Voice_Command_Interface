# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

#importations
from math import *
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import numpy as np
import random
import wave
import winsound
import time
from module_enregistrement import enregistrement as enregistrement
from tri import triSelection as tri
#from serial import Serial
#serial_port = Serial(port='COM5', baudrate=9600) 



def lecture(son):
    #diffuse le signal via les hauts-parleurs 
    winsound.PlaySound(son+'.wav',winsound.SND_FILENAME)
#  
def retardateur(t):
    #tourne dans le vide pendant un temps t
    debut = time.time()
    while time.time() - debut <t:
        a=1
        
"""def instructionArduino(chaine):
    #lettre à entrer par exemple
    serial_port.write(str(chaine).encode('ascii')) #envoi de l'instruction, codée en ascii
    serial_port.readline()#lit ce qu'envoie l'arduino        
"""


##



#fonctions de bases du traitement

def retardateur(t):
    #tourne dans le vide pendant un temps t
    debut = time.time()
    while time.time() - debut <t:
        a=1

def stereotomono(signal):
    #Transforme un signal stéréo en signal mono
    n=len(signal[1])
    t=np.zeros(n)
    for i in range(0,n):
        t[i]=signal[1][i][0]
    signalmono = (signal[0],t)    
    return (signalmono)
    
    
def freq_ech(signal):
    #renvoie la frequence d'échantillonage du signal
    return(float(signal[0]))
    
    
def duree(signal):
    #renvoie la durée du signal en secondes
    return(float(float(len(signal[1])))/freq_ech(signal))
    
    
def matrice_temps(signal):
    # renvoie la matrice de temps associé au signal
    fe = freq_ech(signal) #frequence d'echantillonage
    y = signal[1] #signal sous forme array
    N = float(len(y)) #nombre de points
    x = np.linspace(0.0, N/fe, N)
    return(x)   


def matricetotale_frequence(signal):
    # renvoie une matrice de N//2 frequences, régulierement espacées, de 0 à 22050 valeurs, classiquement
    fe = freq_ech(signal) #frequence d'echantillonage
    y = signal[1] #signal sous forme array
    N = float(len(y)) #nombre de points   
    xf = np.linspace(0.0, 0.5*fe, N/2) #tableau de N/2 valeurs, allant de 0 à (0.5*fe)  
    return(xf)
    

def matricetronquee_frequence(signal):
    #renvoie la matrice des frequences mais seulement jusque 1000 Hz, cad les frequences interessantes
    m_total = matricetotale_frequence(signal)
    return m_total[0:int(1000*(duree(signal)))]
         

def matricetotale_fft(signal):
    #renvoie la fft du signal (ie) fft réel//2
    y = signal[1]
    N = float(len(y))
    yf = fft(y)
    return(np.abs(yf[0:int(N/2)]))
    
    
def matricetronquee_fft(signal):
    #renvoie la du signal seulement jusque 1000 HZ
    yf_total = matricetotale_fft(signal)
    return yf_total[0:int((1000)*(duree(signal)))]
    

def moyenne(liste):
    #calcule la moyenne d'une liste
    n = len(liste)
    somme = 0
    for i in range(n):
        somme += liste[i]    
    return somme/n

##


     
#traitement de la fft

def recherche_max(tableau):
    #renvoie l'indice du maximum et sa valeur
    n = len(tableau)
    imax = 0
    for i in range(n):
        if tableau[i] > tableau[imax]:
            imax = i
    return imax,tableau[imax]    

def frequence_max1(signal):
    #renvoie la frequence du pic maximal de la fft du signal (ie) la frequence principale du signal
    yf = matricetronquee_fft(signal)
    frequences = matricetronquee_frequence(signal)
    imax1 = recherche_max(yf)[0]
    frmax1 = frequences[imax1]
    return frmax1
    
    
def frequence_max2(signal):
    #renvoie la frequence du deuxieme pic
    t = duree(signal)
    frequences = matricetronquee_frequence(signal)
    yf = matricetronquee_fft(signal)
    frmax1 = frequence_max1(signal) 
    cutbas = frmax1 - 25
    cuthaut = frmax1 + 25 #tolerance de 50 Hz
    tab_bas = yf[0:int(cutbas*t)]
    tab_haut = yf[int(cuthaut*t):]
    max_bas = recherche_max(tab_bas)[1]
    max_haut = recherche_max(tab_haut)[1]
    if max_bas > max_haut :
        imax2 = recherche_max(tab_bas)[0]
    else:    
        imax2 = recherche_max(tab_haut)[0] + len(yf[0:int(cuthaut*t)])
    frmax2 = frequences[imax2]
    return frmax2
       
    
def tbl_frequence_max12(liste):
    #renvoie la liste de toutes les frequences max de diférents signaux, pas très utile
    n = len(liste)
    resultats1 = [frequence_max1(liste[i]) for i in range(n)]
    resultats2 = [frequence_max2(liste[i]) for i in range(n)]
    return resultats1,resultats2
    

##



#partie graphique   
 
 
def tracetps(signal):
    #trace le signal en fonction du temps
    x = matrice_temps(signal)
    y = signal[1]
    plt.figure(1)
    plt.plot(x, y)
    plt.grid()
    plt.show()


def tracetps_direct(signal,duree_enregistrement):
    #enrgistre la signal et le trace
    return(trace(enregistrement(signal,duree_enregistrement)))


def tracetotale_fft(signal):
    #trace la fft du signal jusque 22000Hz
    yf = matricetotale_fft(signal) #tableau de la fft de y
    xf = matricetotale_frequence(signal) #tableau de N/2 valeurs, allant de 0 à (0.5*(N))/(N/fe)
    plt.plot(xf, yf) #on ne prend que la moitié du signal, cf doc fft
    plt.grid()
    plt.show()

def tracefft(signal):
    #trace la fft du signal jusque 1000Hz
    yf = matricetronquee_fft(signal)
    xf = matricetronquee_frequence(signal)
    plt.figure(1)
    plt.plot(xf, yf)
    plt.legend()
    plt.xlabel('frequence en Hertz')
    plt.ylabel('amplitude, unité arbitraire')
    plt.grid()
    plt.show()
    
    
def trace(signal):
    #renvoie sur un meme graphique le signal et sa FFT
    plt.figure(1)
    plt.subplot(211)    
    x = matrice_temps(signal)
    y = signal[1]
    plt.plot(x, y, label = 'trace en fonction du temps')
    plt.legend()
    plt.xlabel('temps en secondes')
    plt.grid()
    plt.subplot(212)
    yf = matricetronquee_fft(signal)
    xf = matricetronquee_frequence(signal)
    plt.xlabel('frequence en Hertz')
    plt.plot(xf, yf, label = 'trace de la FFT')
    plt.legend()
    plt.grid()
    plt.show()
    
    
    
def tracemultiple_fft(liste):
    #superpose differentes ffts
    #ex: liste = [i1,i2]
    n = len(liste)
    rang = []
    for i in range(n):
        rang = str([i+1])
        yf = matricetronquee_fft(liste[i])
        xf = matricetronquee_frequence(liste[i])
        r = random.uniform(0,1)
        v = random.uniform(0,1)
        b = random.uniform(0,1)
        plt.plot(xf, yf, color =(r,v,b), label = 'signal'+rang)
        plt.legend()
        plt.title('FFT des differents signaux')
        plt.grid()
        plt.show()
    
        
##



#apprentissage de l'utilisateur

def instructions(phoneme):
    #instructions, pour faire joli
    retardateur(2.0)
    print('reconnaisance du son '+str(phoneme)+' :')
    retardateur(2.0)
    print('produisez le son '+str(phoneme)+' dix fois de suite pendant 1 seconde en suivant les instructions')
    retardateur(4.0)
    print('à vous de jouer!')
    
    
def creationBanque():
    #permet d'attribuer une frequence à un son
    print('Bonjour,je vais apprendre à mieux vous connaître')
    retardateur(2.0)
    nom = input('entrez votre pseudo: ')
    print('Merci, nous allons pouvoir démarrer')
    banque = []
    listePhoneme = []
    a=1 #pipotage de boucle
    while a==1:
        phoneme = input('entrez le son à enregistrer. Si vous avez terminé, tapez stop : ')
        if phoneme =='stop':
            a = 0 #on quitte la boucle
            print('La banque de sons est terminée, à bientôt!')
        else:
            listePhoneme.append(phoneme)
            instructions(phoneme)
            sig = []
            for k in range(10):
                sig.append(enregistrement(phoneme+nom+str(k),1.5))
                retardateur(0.5)
            banque.append(sig)
            print('le son '+phoneme+' a bien été enregistré')
    return listePhoneme, banque
    

def encadrementFrequences(phoneme):
    #retourne les encadrements de frequences pour une liste de 10 phonemes
    tbl = tbl_frequence_max12(phoneme)
    frmax1 = tri(tbl[0])
    if frmax1[8] - frmax1[1] < frmax1[1]: #pas de saut de frequence
        pic1Bas = frmax1[1] - frmax1[1]/5
        pic1Haut = frmax1[8] + frmax1[8]/5
    else:
        milieu = (frmax1[4]+frmax1[5])/2
        if frmax1[8]-milieu > milieu - frmax1[1]:
            pic1Bas = frmax1[1] - frmax1[1]/5
            k = 8
            while frmax1[k]-milieu > milieu - frmax1[1]:
                k = k-1
            pic1Haut = frmax1[k] +frmax1[k]/5   
        else:
            pic1Haut = frmax1[8] + frmax1[8]/5
            k = 1
            while milieu - frmax1[k] > frmax1[8] - milieu:
                k = k+1
            pic1Bas = frmax1[k] - frmax1[k]/5
    frmax2 = tri(tbl[1])
    if frmax2[8] - frmax2[1] < frmax1[1]: #pas de saut de frequence
        pic2Bas = frmax2[1] - frmax2[1]/5
        pic2Haut = frmax2[8] + frmax2[8]/5
    else:
        milieu = (frmax2[4]+frmax2[5])/2
        if frmax2[8]-milieu > milieu - frmax2[1]:
            pic2Bas = frmax2[1] - frmax2[1]/5
            k = 8
            while frmax2[k]-milieu > milieu - frmax2[1]:
                k = k-1
            pic2Haut = frmax2[k] + frmax2[k]/15  
        else:
            pic2Haut = frmax2[8] + frmax2[8]/5
            k = 1
            while milieu - frmax2[k] > frmax2[8] - milieu:
                k = k+1
            pic2Bas = frmax2[k] - frmax2[k]/5
    return [pic1Bas,pic1Haut,pic2Bas,pic2Haut]
    

def frequence_moyenne(phoneme):
    #fais la moyenne de chaque frquence type du phoneme, enleve les valeurs extremes
    tbl = tbl_frequence_max12(phoneme)
    fr1 = tri(tbl[0])
    med = (fr1[4]+fr1[5])/2
    nouv = []
    for i in range(10):
        if abs((fr1[i]-med)/med)<0.5:
            nouv.append(fr1[i])
    frmoy1 = moyenne(nouv)
    fr2 = tri(tbl[1])
    med = (fr2[4]+fr2[5])/2
    nouv = []
    for i in range(10):
        if abs((fr2[i]-med)/med)<0.5:
            nouv.append(fr2[i])
    frmoy2 = moyenne(nouv)
    return [frmoy1, frmoy2]        
            

def traitement_banque_moyenne(banque):
    # applique frequence-moyenne à toute une banque, renvoie une liste de listes de frequences
    n = len(banque[1])
    frequence = []
    for i in range(n):
        frequence.append(frequence_moyenne(banque[1][i]))
    return frequence 
    
def traitement_banque(banque):
    #cherche les pics de chaque phoneme, en enlevant les valeurs extremes
    #banque est une liste de liste de phoneme.
    #i:
    n = len(banque[1])
    encadrement = []
    for i in range(n):
        encadrement.append(encadrementFrequences(banque[1][i]))
    return encadrement #encadrement est une liste de liste contenat quatre caleurs de pics pour chaque phoneme
    
    
def reconnaissance():
    #permet la reconnaissance d'un phonème
    nom = input('Entrez votre pseudo: ')
    if nom == 'etienne':
        banque = banque_etienne
    elif nom == 'jb':
        banque = banque_jb
    else:
        print('cest votre première utilsation, il va falloir vous enregistrer')
        banque = creationBanque()
    print('données en traitement..."')
    donnee = traitement_banque(banque)  
    print('La reconnaissance vocale va pouvoir démarrer')
    while True:
        arret = input('si vous voulez arrêter, tapez stop, sinon tapez entrée : ')
        if arret == 'stop':
            return ("merci d'avoir utilisé notre service")
        son = enregistrement('echantillon', 1.5)
        frmax1 = frequence_max1(son)
        frmax2 = frequence_max2(son)
        listePhoneme = banque[0]
        n = len(listePhoneme)
        identification = False
        for i in range(n):
            d = donnee[i] 
            if  (d[0]< frmax1 < d[1] and d[2] < frmax2 < d[3]) or (d[0]< frmax2 < d[1] and d[2] < frmax1 < d[3]):
                print('vous avez pronnoncé le son : ', listePhoneme[i])
                identification = True
        if identification == False:        
            print('signal non identifié')
        print(frmax1,frmax2)    


def t(pivot,pourcentage):
    #pivot le nombre autour de la tolerance
    return (pourcentage/100)*pivot
    
    
def reconnaissance2():
    #permet la reconnaissance d'un phonème
    nom = input('Entrez votre pseudo: ')
    if nom == 'etienne':
        banque = banque_etienne
    elif nom == 'jb':
        banque = banque_jb
    else:
        print('cest votre première utilsation, il va falloir vous enregistrer')
        banque = creationBanque()
    print('données en traitement..."')
    donnee = traitement_banque_moyenne(banque)
    print('La reconnaissance vocale va pouvoir démarrer')
    while True:
        arret = input('si vous voulez arrêter, tapez stop, sinon tapez entrée : ')
        if arret == 'stop':
            return ("merci d'avoir utilisé notre service")
        son = enregistrement('echantillon', 1.5)
        f1 = frequence_max1(son)
        f2 = frequence_max2(son)
        listePhoneme = banque[0]
        n = len(listePhoneme)
        p = 20 #pourcentage de precision
        identification = False
        for i in range(n):
            d = donnee[i]
            if  (d[0]-t(f1,p)< f1 < d[0]+t(f1,p) and d[1]-t(f2,p) < f2 < d[1]+t(f2,p)) or (d[0]-t(f2,p)< f2 < d[0]+t(f2,p) and d[1]-t(f1,p) < f1 < d[1]+t(f1,p)):
                print('vous avez pronnoncé le son : ', listePhoneme[i])
                identification = True
        if identification == False:        
            print('signal non identifié')
        print(f1,f2)    

def reconnaissanceArduino():
    #reconnait un son, le clou du programme, la cerise sur le gateau, la creme de la creme et envoie l'instruction a l'arduino, sous forme d'une lettre(chaine de caractere)
    nom = input('Entrez votre pseudo: ')
    if nom == 'etienne':
        banque = banque_etienne
        print('bonjour etienne')
    elif nom == 'jb':
        banque = banque_jb
        print('bonjour jb')
    else:
        print('cest votre première utilsation, il va falloir vous enregistrer')
        banque = creationBanque()
    print('données en traitement...')
    donnee = traitement_banque(banque[1])  
    print('La reconnaissance vocale va pouvoir démarrer')
    retardateur(2)  
    while True:
        arret = input('si vous voulez arrêter, tapez stop, sinon tapez entrée : ')
        if arret == 'stop':
            instructionArduino('s')
            return ("merci d'avoir utilisé notre service")
        son = enregistrement('echantillon', 1.5)
        frmax1 = frequence_max1(son)
        frmax2 = frequence_max2(son)
        listePhoneme = banque[0]
        n = len(listePhoneme)
        identification = False
        for i in range(n):
            d = donnee[i] 
            if  (d[0]< frmax1 < d[1] and d[2] < frmax2 < d[3]) or (d[0]< frmax2 < d[1] and d[2] < frmax1 < d[3]):
                print('vous avez pronnoncé le son : ', listePhoneme[i])
                instructionArduino(listePhoneme[i])
                identification = True
        if identification == False:        
            print('signal non identifié')
        print('maxs indicatifs : ',frmax1,frmax2) # à titre indicatif           
        retardateur(2)

            
    
##




#signaux utilisés


#jb

#i
i0 = read('ijb0.wav')
i1 = read('ijb1.wav')
i2 = read('ijb2.wav')
i3 = read('ijb3.wav')
i4 = read('ijb4.wav')
i5 = read('ijb5.wav')
i6 = read('ijb6.wav')
i7 = read('ijb7.wav')
i8 = read('ijb8.wav')
i9 = read('ijb9.wav')
i_jb = [i0,i1,i2,i3,i4,i5,i6,i7,i8,i9]

#o
o0 = read('ojb0.wav')
o1 = read('ojb1.wav')
o2 = read('ojb2.wav')
o3 = read('ojb3.wav')
o4 = read('ojb4.wav')
o5 = read('ojb5.wav')
o6 = read('ojb6.wav')
o7 = read('ojb7.wav')
o8 = read('ojb8.wav')
o9 = read('ojb9.wav')
o_jb = [o0,o1,o2,o3,o4,o5,o6,o7,o8,o9]

#a
a0 = read('ajb0.wav')
a1 = read('ajb1.wav')
a2 = read('ajb2.wav')
a3 = read('ajb3.wav')
a4 = read('ajb4.wav')
a5 = read('ajb5.wav')
a6 = read('ajb6.wav')
a7 = read('ajb7.wav')
a8 = read('ajb8.wav')
a9 = read('ajb9.wav')
a_jb = [a0,a1,a2,a3,a4,a5,a6,a7,a8,a9]


banque_jb = [['i','o','a'],[i_jb,o_jb,a_jb]]


#etienne

#i
ii0 = read('ietienne0.wav')
ii1 = read('ietienne1.wav')
ii2 = read('ietienne2.wav')
ii3 = read('ietienne3.wav')
ii4 = read('ietienne4.wav')
ii5 = read('ietienne5.wav')
ii6 = read('ietienne6.wav')
ii7 = read('ietienne7.wav')
ii8 = read('ietienne8.wav')
ii9 = read('ietienne9.wav')
i_etienne = [ii0,ii1,ii2,ii3,ii4,ii5,ii6,ii7,ii8,ii9]
imoy=[120,250]

#a
aa0 = read('aetienne0.wav')
aa1 = read('aetienne1.wav')
aa2 = read('aetienne2.wav')
aa3 = read('aetienne3.wav')
aa4 = read('aetienne4.wav')
aa5 = read('aetienne5.wav')
aa6 = read('aetienne6.wav')
aa7 = read('aetienne7.wav')
aa8 = read('aetienne8.wav')
aa9 = read('aetienne9.wav')
a_etienne = [aa0,aa1,aa2,aa3,aa4,aa5,aa6,aa7,aa8,aa9]
amoy=[125,600]

#o
oo0 = read('oetienne0.wav')
oo1 = read('oetienne1.wav')
oo2 = read('oetienne2.wav')
oo3 = read('oetienne3.wav')
oo4 = read('oetienne4.wav')
oo5 = read('oetienne5.wav')
oo6 = read('oetienne6.wav')
oo7 = read('oetienne7.wav')
oo8 = read('oetienne8.wav')
oo9 = read('oetienne9.wav')
o_etienne = [oo0,oo1,oo2,oo3,oo4,oo5,oo6,oo7,oo8,oo9]
omoy=[380,125]

banque_moy = [['i','o','a'],[imoy,omoy,amoy]]
banque_etienne = [['i','o','a'],[i_etienne,o_etienne,a_etienne]]

       
##
    
    
