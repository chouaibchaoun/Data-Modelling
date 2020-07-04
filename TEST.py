import os
import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt

start = timeit.default_timer()

os.chdir("C:\\Users\\choua\\Documents\\études\\projet enjeux\\HISTORIQUE DE CONSAMMATION\\test") #Go to the file's path



L = [1.70 , 1.67 , 1.85 , 1.79 , 1.50,1.45,1.40,1.35,1.30,1.27,1.24,1.20,1.17,1.14,1.10,1.07,1.03,1.00,0.97,0.94,0.90,0.87,0.84,0.80,0.77,0.74,0.70,0.67,0.64,0.60,0.55,0.50,0.45,0.40,0.35,0.33,0.30,0.24]

L.sort()

def rappro(x , L = L ) :
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
    
    
    





x = pd.read_csv("2015.csv"  ) #uploading data
x.columns = ["A"] #changing the name of the column because spaces in names are disfunctional
E = [] ; S = [] ; En = [] #creating Blank lists
D={} #dictionary to filter data

for i in range (x.A.count()) : #converting data from DataFrame to lists


    m = x.iloc[i][0].split(";") #Split it to tree numbers
    if m[2] == "" or m[2] == 0 : #Get ride of blank values of energy
        continue
    if m[3] == "" or m[3] == 0 : #Get ride of blank values of energy
        continue
    
    # float(m[0]) Epaisseur d'entree 
    # float(m[1]) Epaisseur de sortie
    # float(m[2]) Energie consommée 
    # float(m[3]) PoidsNet de la bobine
    # (float(m[2])/float(m[3]))*1000 Energie consommée par tonne 
        
    E = E + [float(m[0])]
    En = En + [(float(m[2])/float(m[3]))*1000]
    S = S + [float(m[1])]
    
    # Pour chaque sortie on associe les différentes entrées possibles et l'énergie qu'ils ont consommées par tonne.
    if ( float(m[0]) , rappro(float(m[1])) ) in D.keys() :
        D[float(m[0]) , rappro(float(m[1]))] = D[ float(m[0]) , rappro(float(m[1])) ] + [ (float(m[2])/float(m[3]))*1000 ]
    else :
        D[ float(m[0]) , rappro(float(m[1])) ] = [(float(m[2])/float(m[3]))*1000 ]
    

x = pd.DataFrame({}) #creating a new DataFrame to avoid size problems


#uploading data to the new DataFrame

x ["entre"] = E 
x ["sortie"] = S
x ["EnP"] = En

X = [] ; Y = []

ent = float(input("Entrer l'épaisseur d'entrée : "))
sor = float(input("Entrer l'épaisseur de sortie : "))

while not (ent , sor) in D.keys() :
    print("__________entrer des valeurs valides__________")
    ent = float(input("Entrer l'épaisseur d'entrée : "))
    sor = float(input("Entrer l'épaisseur de sortie : "))


for i in range(len(D[ent, sor])):
    X = X + [i]
    Y = Y + [D[ent, sor][i]]
    
    
plt.scatter(X,Y)
plt.show()

    


stop = timeit.default_timer()
print('Time: ', stop - start)

