# =============================================================================
# # import libraries
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
import math
from operator import itemgetter
import random as rd

from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap 
import pyproj


# =============================================================================
# =============================================================================
# # PARAMÈTRES DU PROBLÈME
# =============================================================================
# =============================================================================
C=[100,100]               # Coordonnées du point de largage initial
vec=[5,10]              # Vecteur directeur du largage suivant x et y 

# Mat_x=fx                # Taille de la matrice suivant x (même dimension que fx la matrice du combustible =>511)
# Mat_y=fy                # Taille de la matrice suivant y (même dimension que fy la matrice du combustible =>682)

t_largage=[0,10,0]      # Heure du largare au format [heure,minute,seconde]

Dt=[0,20,0]             # Durée entre 2 largages successifs au format [heure,minute,seconde]

Nb_largage = 1         # Nombre de largage sur la zone 
                 

# =============================================================================
# =============================================================================
# # OUVERTURE DU FICHIER landscape.nc
# =============================================================================
# =============================================================================

data = Dataset("/home/bthoby/firefront-master/examples/aullene/landscape.nc")
# print(data.variables.keys())

# print(data)

parameters = data['parameters'][:]
domain  = data['domain']
wind = data['wind']
fuel = data['fuel'][:]
altitude = data['altitude']

SWx = domain.__dict__['SWx']
SWy = domain.__dict__['SWy']

Lx = domain.__dict__['Lx']
Ly = domain.__dict__['Ly']

fx = len(fuel[0,0,0,:])
fy = len(fuel[0,0,:,0])

EPSG = (data.__dict__['projection'])

background = fuel[0,0,:,:]
altitude = altitude[0,0,:,:]




Mat_x=fx
Mat_y=fy 


# =============================================================================
# =============================================================================
# # FONCTIONS 
# =============================================================================
# =============================================================================

# Transforme un format [heure,minute,seconde] en seconde 
def seconde(T):
    return 3600*T[0] + 60*T[1] + T[2]

# Transforme un format seconde en [heure,minute,seconde]
def heure(t):
    T=[0,0,0]
    T[0] = t//3600
    reste = t%3600
    T[1] = reste//60
    T[2] = reste%60
    return T

        
# =============================================================================
# #Calcul de l'angle en dégré du vecteur directionel

# L'angle va de 0 à 360 degrés suivant le cercle trigo
# =============================================================================
def angle(vec):                     
    if vec[0]==0:
        if vec[1]>0:
            alphaD=90
        elif vec[1]<0:
            alphaD=270
    else:
        alphaR=math.atan(vec[1]/vec[0])
        if vec[0]<0:
            alphaD=math.degrees(alphaR)+180
        elif vec[0]>0:
            if alphaR>0:
                alphaD=math.degrees(alphaR)
            else:
                alphaD=math.degrees(alphaR)+360
    if (alphaD)==360:
        alphaD=0
    return(alphaD)
            


#Définir les points en fonction de k, la distance au centre 

def points(k):
    Liste=[]
    if k>0:
        L=np.arange(-k, k+1)
        g=L[0]
        d=L[-1]
        for j in L:
            Liste.append([g,j])
            Liste.append([d,j])
        for i in range(L[1],L[-1]):
            Liste.append([i,g])
            Liste.append([i,d])
        Liste.sort()
        
    return(Liste)


# Renvoie les pixels qui seront coloriés en fonction de l'angle du vecteur directeur et de la distance au centre
def choixpoints(vec,k):
    Liste=points(k)
    alpha=angle(vec)
    m=int(len(Liste)/2)
# =============================================================================
#     PARTIE GAUCHE
# =============================================================================
    # PARTIE GAUCHE             
    if (90<alpha<270): 
        Liste=Liste[:m+1]
        
# =============================================================================
#          PARTIE HAUT GAUCHE                            
# =============================================================================
        if (90<alpha<180):                            
            m=int(len(Liste)/2)
            Liste=sorted(Liste, key=itemgetter(1))
            Liste=Liste[m:]
            if (150<alpha<180):
                Liste=sorted(Liste, key=itemgetter(0))
                m=int(len(Liste)/2)
                Liste=Liste[:m+1]
                if (k>1):
                    Liste.pop(-1)
                    if (alpha>165):
                        if (k>2):
                            Liste.pop(-1)
                            if (k>3):
                                Liste.pop(-1)
                    else:
                        if (k>2):
                            Liste.pop(0)
                            if (k>3):
                                Liste.pop(0)
            if (120<alpha<150):                         
                if (k>1):
                    Liste.pop(0)
                    Liste.pop(-1)
                    if (k>2):
                        Liste.pop(0)
                        Liste.pop(-1)
                        if (k>3):
                            Liste.pop(0)
                            Liste.pop(-1)
                if (alpha<135):
                    Liste=sorted(Liste, key=itemgetter(0))
                    Liste.pop(0)
                if (alpha>135):
                    Liste=sorted(Liste, key=itemgetter(1))
                    Liste.pop(-1)
            if (90<alpha<120):
                m=int(len(Liste)/2)
                Liste=sorted(Liste, key=itemgetter(1))
                Liste=Liste[m:]
                if (k>1):
                    Liste.pop(0)
                    if (alpha<105):
                        if (k>2):
                            Liste.pop(0)
                            if (k>3):
                                Liste.pop(0)
                    else :
                        if (k>2):
                            Liste.pop(-1)
                            if (k>3):
                                Liste.pop(-1)
                       
# =============================================================================
#         PARTIE BAS GAUCHE                                     
# =============================================================================
        if (180<alpha<270):
            Liste=sorted(Liste, key=itemgetter(1))
            m=int(len(Liste)/2)
            Liste=Liste[:m+1]
            
            if (180<alpha<210):                                 
                Liste=sorted(Liste, key=itemgetter(0))
                m=int(len(Liste)/2)
                Liste=Liste[:m+1]
                if (k>1):
                    Liste.pop(0)
                    if (alpha>195):
                        if (k>2):
                            Liste.pop(-1)
                            if (k>3):
                                Liste.pop(-1)
                    else:
                        if (k>2):
                            Liste.pop(0)
                            if (k>3):
                                Liste.pop(0)
            if (210<alpha<240):                                 
                if (k>1):
                    Liste.pop(-1)
                    Liste=sorted(Liste, key=itemgetter(0))
                    Liste.pop(-1)
                    if (k>2):
                        Liste.pop(-1)
                        Liste=sorted(Liste, key=itemgetter(1))
                        Liste.pop(-1)
                        if (k>3):
                            Liste.pop(-1)
                            Liste=sorted(Liste, key=itemgetter(0))
                            Liste.pop(-1)
                if (alpha<225):
                    Liste=sorted(Liste, key=itemgetter(0))
                    Liste.pop(-1)
                if (alpha>225):
                    Liste=sorted(Liste, key=itemgetter(1))
                    print('L2=', Liste)
                    Liste.pop(-1)
            if (240<alpha<270):
                m=int(len(Liste)/2)
                Liste=Liste[:m+1]
                if (k>1):
                    Liste.pop(0)
                    if (alpha>255):
                        if (k>2):
                            Liste.pop(0)
                            if (k>3):
                                Liste.pop(0)
                    else :
                        if (k>2):
                            Liste.pop(-1)
                            if (k>3):
                                Liste.pop(-1)
       
# =============================================================================
#     PARTIE HAUT DROITE                               
# =============================================================================
    elif (0<alpha<90):
        Liste=Liste[m-1:]
        m=int(len(Liste)/2)
        Liste=sorted(Liste, key=itemgetter(1))
        Liste=Liste[m:]
        if (0<alpha<30):
            Liste=sorted(Liste, key=itemgetter(0))
            m=int(len(Liste)/2)
            Liste=Liste[m:]
            if (k>1):
                Liste.pop(-1)
                if (alpha<15):
                    if (k>2):
                        Liste.pop(-1)
                        if (k>3):
                            Liste.pop(-1)
                else:
                    if (k>2):
                        Liste.pop(0)
                        if (k>3):
                            Liste.pop(0)
        if (30<alpha<60):
            if (k>1):
                Liste.pop(0)
                Liste=sorted(Liste, key=itemgetter(0))
                Liste.pop(0)
                if (k>2):
                    Liste.pop(0)
                    Liste=sorted(Liste, key=itemgetter(1))
                    Liste.pop(0)
                    if (k>3):
                        Liste.pop(0)
                        Liste=sorted(Liste, key=itemgetter(0))
                        Liste.pop(0)
            if (alpha<45):
                Liste=sorted(Liste, key=itemgetter(0))
                Liste.pop(0)
            if (alpha>45):
                Liste=sorted(Liste, key=itemgetter(1))
                Liste.pop(0)
        if (60<alpha<90):
            Liste.pop(0)
            m=int(len(Liste)/2)
            Liste=sorted(Liste, key=itemgetter(1))
            Liste=Liste[m-1:]
            if (k>1):
                Liste.pop(-1)
                if (alpha<75):
                    if (k>2):
                        Liste.pop(0)
                        if (k>3):
                            Liste.pop(0)
                else :
                    if (k>2):
                        Liste.pop(-1)
                        if (k>3):
                            Liste.pop(-1)
    
# =============================================================================
#     PARTIE BAS DROITE                                 
# =============================================================================
    elif (270<alpha<360):
        Liste=Liste[m-1:]
        m=int(len(Liste)/2)
        Liste=sorted(Liste, key=itemgetter(1))
        Liste=Liste[:m+1]
        if (330<alpha<360):
            m=int(len(Liste)/2)
            Liste=Liste[m:]
            if (k>1):
                Liste.pop(0)
                if (alpha>345):
                    if (k>2):
                        Liste.pop(0)
                        if (k>3):
                            Liste.pop(0)
                else:
                    if (k>2):
                        Liste.pop(-1)
                        if (k>3):
                            Liste.pop(-1)         
        if (300<alpha<330):
            if (k>1):
                Liste.pop(0)
                Liste.pop(-1)
                if (k>2):
                    Liste.pop(0)
                    Liste.pop(-1)
                    if (k>3):
                        Liste.pop(0)
                        Liste.pop(-1)
            if (alpha<315):
                Liste=sorted(Liste, key=itemgetter(0))
                Liste.pop(-1)
            if (alpha>315):
                Liste=sorted(Liste, key=itemgetter(1))
                Liste.pop(0)
        if (270<alpha<300):
            m=int(len(Liste)/2)
            Liste=Liste[:m+1]
            if (k>1):
                Liste.pop(-1)
                if (alpha<285):
                    if (k>2):
                        Liste.pop(-1)
                        if (k>3):
                            Liste.pop(-1)
                else:
                    if (k>2):
                        Liste.pop(0)
                        if (k>3):
                            Liste.pop(0)
# =============================================================================
#     POINTS PARTICULIERS
# =============================================================================
    elif (alpha==90):
        Liste=[[0,k]]
    
    if (alpha==180):
        print('L2=', Liste)
        Liste=[[-k,0]]
 
    elif (alpha==270):
        Liste=[[0,-k]]
        
    elif (alpha==0):
        Liste=[[k,0]]
    
    return(Liste)







# =============================================================================
# Matrice de pixels avec l'heure d'arrivée du largage 
# =============================================================================
A=np.zeros((Mat_x,Mat_y))


# =============================================================================
# FONCTION PRINCIPALE
# Renvoie la matrice du sol avec les pixels touchés par le largage 
# Matrice remplie de 0, avec au niveau du largage des pixels qui ont pour valeur l'heure en seconde du largage sur cette zone
# =============================================================================

def largage(A,T,C,vec):
    
    t=seconde(T)
    
    x0,y0=C[0],C[1]
    A[x0,y0]=t
    
    for k in range(1,5):
        Liste=choixpoints(vec, k)
        for i in range(len(Liste)):
            indice_x=Liste[i][0]
            indice_y=Liste[i][1]
            A[x0+indice_x,y0+indice_y]=t+k
   
    return(A)



# =============================================================================
# EXÉCUTION DE PLUSIEURS LARGAGES SUCCESIFS
# =============================================================================

def differents_largages(A,C,vec,T,Dt,Nb):
    t = seconde(T)
    dt = seconde(Dt)
    A = largage(A, T, C, vec)
    Donnees=[]
    Donnees.append([T,C,angle(vec)])
    for i in range(1,Nb):
        tps = t + i*dt
        C_x = rd.randint(-4,4)
        C_y = rd.randint(-4,4)
        vec_x = rd.randint(-3,3)
        vec_y = rd.randint(-3,3)
        TPS=heure(tps)
        Donnees.append([TPS,[C[0]+C_x,C[1]+C_y],angle([vec[0]+vec_x,vec[1]+vec_y])])
        A = largage(A, TPS, [C[0]+C_x,C[1]+C_y], [vec[0]+vec_x,vec[1]+vec_y])
    return A, Donnees





# =============================================================================
# ECRITURE DES TRIGGER
# =============================================================================


if (Nb_largage<2):
    Mat_A = largage(A, t_largage, C, vec)
else:
    Mat_A,Donnees = differents_largages(A,C,vec,t_largage,Dt,Nb_largage)
Mat_A=np.transpose(Mat_A)

fichier = open("trigger.txt", 'w')

for i in range (len(Mat_A)):
    for j in range (len(Mat_A[0])):
        if (Mat_A[i][j]>0):
            Coordx = SWx + i * Lx / fx
            Coordy = SWy + j * Ly / fy
            time = Mat_A[i][j]
            
            fichier.write('trigger[fuelIndice];loc=(')
            fichier.write(str(Coordx))
            fichier.write(',')
            fichier.write(str(Coordy))
            fichier.write(',0);fuelType=0]@t=')
            fichier.write(str(time))
            fichier.write('\n')
fichier.close()
            
            
            













# =============================================================================
# PLOT DE LA MATRICE 
# =============================================================================
 
# B=str(int(angle(vec)))
# Mat_A = largage(A, t_largage, C, vec)
# plt.figure("Un largage")
# plt.imshow(np.transpose(Mat_A), origin='lower', vmin=seconde(t_largage)-1, vmax=Mat_A.max())
# plt.colorbar(label='Temps en seconde des largages')
# plt.xlabel('X')
# plt.ylabel('Y')

# plt.title("Un largage au point " +str(C) +" et d'angle de largage "  + B +"°" )

# plt.show()


# # =============================================================================
# # PLOT DES DIFFERENTS LARGAGES SUCCESSIFS 
# # =============================================================================
    
# if (Nb_largage>1):
#     Dif_A,Donnees = differents_largages(A,C,vec,t_largage,Dt,Nb_largage)
#     for i in range(Nb_largage):
#         print('Largage numéro ',i+1)
#         print('Heure du largage :', Donnees[i][0], ' [heure,minute,seconde]', '\nCoordonnée du largage :', Donnees[i][1], '\nAngle du largage : ', Donnees[i][2])
#         print('')
#     plt.figure("Plusieurs largages")
#     plt.imshow(np.transpose(Dif_A), origin='lower', vmin=0, vmax=Dif_A.max())
#     plt.colorbar(label='Temps en seconde des largages')
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     plt.title(str(Nb_largage)+" largages avec " +str(seconde(Dt)) +" secondes d'écarts entre chaque." )
#     plt.show()


# =============================================================================
# PLOT AVEC LA SUPERPOSITION DU CHAMP FUEL 
# =============================================================================
plt.figure("Superposition du champ fuel avec la matrice de largage")


# A=np.zeros((Mat_x,Mat_y))
Mat=np.zeros((Mat_x,Mat_y))

# Mat_A = largage(A, t_largage, C, vec)
A=np.transpose(A)
for i in range(len(A)):
    for j in range (len(A[0])):
        Mat = background
        if (A[i][j])>0:
            Mat[i][j] = A[i][j]
        
plt.imshow(Mat, origin='lower')
plt.colorbar(label='Temps en seconde des largages')
plt.xlabel('X')
plt.ylabel('Y')

# penser a modifier les couleurs car après plusieurs simu on ne voit plus le fond

plt.show()







