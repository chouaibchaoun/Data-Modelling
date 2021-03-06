import os
import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#os.chdir("C:\\Users\\choua\\Documents\\études\\projet enjeux\\HISTORIQUE DE CONSAMMATION\\test") #Go to the file's path")


#définir les listes convenable à chaque catégorie

Lext_Doux = [2 , 1.90 , 1.80 , 1.70 , 1.65 , 1.60 , 1.55 , 1.50,1.45,1.40,1.35,1.30,1.27,1.24,1.20,1.17,1.14,1.10,1.07,1.03,1.00,0.97,0.94,0.90,0.87,0.84,0.80,0.77,0.74,0.70,0.67,0.64,0.60,0.55,0.50,0.45,0.40,0.35,0.33,0.30,0.28 , 0.25 , 0.23 ]

Lext_const=[2 , 1.80 , 1.75 , 1.65 , 1.50,1.45,1.30,1.20,1.00,0.90]

LM_Doux=[1.70 , 1.67 , 1.85 , 1.79 , 1.50,1.45,1.40,1.35,1.30,1.27,1.24,1.20,1.17,1.14,1.10,1.07,1.03,1.00,0.97,0.94,0.90,0.87,0.84,0.80,0.77,0.74,0.70,0.67,0.64,0.60,0.55,0.50,0.45,0.40,0.35,0.33,0.30,0.24]

LM_const=[2 , 1.80 , 1.75 , 1.65 , 1.50,1.45,1.30,1.20,1.00,0.90]


#interface 
def interface() :
    print("Type du fichier: ")
    print("1. Maghrebsteel_Doux")
    print("2. Maghrebsteel_construction")
    print("3. Ext_Doux")
    print("4. Ext_construction")
    return int(input("Préciser la catégorie du fichier à traiter : "))

i = int(input("Changer l'emplacement de votre fichier : \n1.Oui    \n2.Non    \n"))
if i == 1 : 
    loc = str(input("Enter la location du fichier à traiter : "))
    os.chdir(loc)
    
categ = interface()

while not categ in [1,2,3,4]:
    print("entrez un choix valide")
    categ = interface()   

fichentr = str(input("Entrer le nom du fichier à traiter  :   "))


#acccorder votre choix au fichier et liste convenable
if categ == 1 :
    out = "out_M_Doux.csv"
    L = LM_Doux
elif categ == 2:
    out = "out_M_const.csv"
    L = LM_const
elif categ == 3:
    out = "out_Ext_Doux.csv"
    L = Lext_Doux
elif categ == 4:
    out = "out_Ext_const.csv"
    L = Lext_const


L.sort()



def average(L):   #elle prend une liste et donne la valeur moyenne de tous ces valeurs
    m=0
    for i in range(len(L)):
        m = m + L[i]
    m = m/len(L)
    return m

def Delete_items(L,Del): #prend en paramètre deux liste, 1er des données, 2eme des index à supprimer.
    Del.sort()
    for i in range(len(Del)) :
        L.remove(L[int(Del[i])-1])
    return

def rappro(x , L = L ) : #en se basant sur une liste L donnée, elle rapproche la valeur x à une valeur dans L
    m=0
    for i in range(len(L)-1):
        if L[i] <= x and x < L[i+1] :
            m=i
            break
    p = abs(L[m] - x)
    i = abs(L[m+1] - x)
    if p < i :
        return L[m]
    return L[m+1]
    
    
    





x = pd.read_csv(fichentr) #uploading data
x.columns = ["A"] #changing the name of the column because spaces in names are disfunctional
E = [] ; S = [] ; En = [] ; Larg = [] #creating Blank lists
D={} #dictionary to filter data

for i in range (x.A.count()) : #converting data from DataFrame to lists


    m = x.iloc[i][0].split(";") #Split it to tree numbers
    if m[2] == "" or float(m[2]) == 0 : #Get ride of blank values of energy
        continue
    if m[3] == "" or float(m[3]) == 0 : #Get ride of blank values of energy
        continue
    
    # float(m[0]) Epaisseur d'entree 
    # float(m[1]) Epaisseur de sortie
    # float(m[2]) Energie consommée 
    # float(m[3]) PoidsNet de la bobine
    # float(m[4]) Largeur de la bobine
    # (float(m[2])/float(m[3]))*1000 Energie consommée par tonne 
        
    E = E + [float(m[0])]
    En = En + [(float(m[2])/float(m[3]))*float(m[4])]
    S = S + [float(m[1])]
    
    # Pour chaque sortie on associe les différentes entrées possibles et l'énergie qu'ils ont consommées par tonne.
    if ( float(m[0]) , rappro(float(m[1])) ) in D.keys() :
        D[float(m[0]) , rappro(float(m[1]))] = D[ float(m[0]) , rappro(float(m[1])) ] + [ 1000000*float(m[2])/(float(m[3])*float(m[4])) ]
    else :
        D[ float(m[0]) , rappro(float(m[1])) ] = [1000000*float(m[2])/(float(m[3])*float(m[4])) ]
    

x = pd.DataFrame({}) #creating a new DataFrame to avoid size problems


#uploading data to the new DataFrame

x ["entre"] = E 
x ["sortie"] = S
x ["EnP"] = En


rep=0

#Boucle de filtrage

for (ent,sor) in D.keys() :
  
    rep = rep +1
    if len(D[ent,sor]) < 5 :  #condition sur la quantité de  données initiale
        continue
    D[ent,sor].sort()
    
    #présenter les données qu'on a par défault
    
    X = [] ; Y = []
    

    #Eliminer les données non désirées
    ecart = 5
    j=0
    Lt = []
    L = D[ent , sor ]
    
    
    
    for i in range(len(L)) :
        if i == len(L)-1 :
            Lt = Lt + [L[j:i+1]]
            break

        
        diff = L[i+1] -L[i]

        if diff >= ecart :
            Lt = Lt + [L[j:i+1]]
            j = i+1
    
    
    
    j = 0
    if Lt != [] :
        for i in range(len(Lt)):
            if len(Lt[i]) > len(Lt[j]) :
                j=i
        if len(Lt[j]) < 3 : #condition sur la quantité de données sorties
            continue
        D [ent , sor ] = Lt[j]
    
    


    
#Stocker les données filtrés dans un fichier csv
    
X = [] ; Y = [] ; Z = []
    
for elt in D.keys() :
    X = X + [elt[0]]    
    Y = Y + [elt[1]]
    Z = Z + [average(D[elt[0],elt[1]])]
    
    
# Ded = {"entree" : [] , "sortie" : [] , "Energie Moy" : [] }

y = pd.DataFrame({} ) 
y["entree"] = X
y["Sortie"] = Y
y["Constante K"] = Z  



y.to_csv(out, sep='\t', encoding='utf-8')  



