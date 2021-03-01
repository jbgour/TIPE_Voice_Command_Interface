#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

#Tris simple, cf cours

def plusGrand(a,b):
    return a>b
    
def echange(liste,i,j):
    temp = liste[i]
    liste[i] = liste[j]
    liste[j] = temp
    
def minimumDepuis(liste,i):
    kMin = i
    n = len(liste)
    for k in range(i+1,n):
        if plusGrand(liste[kMin],liste[k]):
            kMin = k
    return kMin
    
def triSelection(liste):
    n = len(liste)
    for i in range(n):
        k = minimumDepuis(liste,i)
        echange(liste,i,k)
    return liste    
  