#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

#importations

from math import *
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import numpy as np
import pyaudio
import wave
import time

##


#compteurs

def decompte_3sec():
    #lance un decompte de 3 sec avant le démarrage
    debut = time.time()
    print('demarrage enregistrement dans:')
    print('3 secondes')
    while time.time()-debut<1:
        a=1
    print('2 secondes')
    debut2 = time.time()
    while time.time()-debut2<1:
        a=1
    print('1 seconde')
    debut3 = time.time()
    while time.time()-debut3<1:
        a=1   
    print('demarrage!')
    

##


         
#module d'enregistrement

QUANTIF = 1024 #codage sur 10 bits
FORMAT = pyaudio.paInt16 #paInt8
CANAL = 1 #enregistrement en mono
FE = 44100 #frequence d'echantillonage
         
        
def enregistrement(nom_de_sortie,duree):
    #enregistre un signal pendant une certaine durée, enregistré en wav
    #renvoie le signal sous un tableau array
    #le nom de sortie est entre '', la durée un flottant
    DUREE = duree #durée de l'enregistrement en secondes
    NOM_SORTIE = nom_de_sortie
    p = pyaudio.PyAudio()
    decompte_3sec()
    stream = p.open(format=FORMAT,
                channels=CANAL,
                rate=FE,
                input=True,
                frames_per_buffer=QUANTIF) #buffer
    frames = []
    for i in range(0, int(FE / QUANTIF * DUREE)):
        data = stream.read(QUANTIF)
        frames.append(data) # 2 bytes(16 bits) per channel
    stream.stop_stream()
    stream.close()
    p.terminate()
    print('enregistrement termine')
    wf = wave.open(NOM_SORTIE+'.wav', 'wb') #https://docs.python.org/2/library/wave.html
    wf.setnchannels(CANAL)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(FE)
    wf.writeframes(b''.join(frames))
    wf.close()
    sortie = read(NOM_SORTIE+'.wav')
    sortie_tronquee = (sortie[0],sortie[1][2000:])#bug au début(environ 0.004s), d'où on le dégage
    trace(sortie_tronquee,NOM_SORTIE)
    return sortie_tronquee

###############################################################################

#fonctions de bases du traitement
   
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
    xf = np.linspace(0.0, 0.5*fe, N/2) #tableau de N/2 valeurs, allant de 0 à (0.5*(N))/(N/fe)  
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
    
         
    
    
###############################################################################



#partie graphique   

def trace(signal,nom):
    #renvoie sur un meme graphique le signal et sa FFT
    plt.figure(1)
    plt.subplot(211)    
    x = matrice_temps(signal)
    y = signal[1]
    plt.plot(x, y, label = 'trace de '+nom)
    plt.legend()
    plt.xlabel('temps en secondes')
    plt.grid()
    plt.subplot(212)
    yf = matricetronquee_fft(signal)
    xf = matricetronquee_frequence(signal)
    plt.xlabel('frequence en Hertz')
    plt.plot(xf, yf, label = 'FFT de '+nom)
    plt.legend()
    plt.grid()
    plt.show()
    
    




       
    
    

