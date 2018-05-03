# -*- coding: utf-8 -*-
from math import acos
from math import sqrt
from cste import *
from simulation.basiques.cube import Cube
from simulation.basiques.balise import Balise
#from simulation.basiques.mur import Mur
#from simulation.basiques.sol import Sol

class Arene :
    """ Classe Arene caracterisée par les attributs:
    - lx : sa limite (double) sur l'axe des x
    - ly : sa limite (double) sur l'axe des y
    - lz : sa limite (double) sur l'axe des z
    - cubes : une liste contenant des "cubes"(sol,mur,obstacle) avec leurs coordonnées dans l'arene
    """

    def __init__(self,lx,ly,lz,cubes=[],robots=[], balises=[]):
        self.lx = lx
        self.ly = ly
        self.lz = lz
        self.cubes = cubes
        self.robots = robots
        self.balises = balises

    def append(self,obj) :
        """Si c'est possible on ajoute un cube dans l'arene
            et on return True, et False sinon"""
        if isinstance(obj, Cube):
            bx = 0<=obj.x and obj.x <= self.lx
            by = 0<=obj.y and obj.y <= self.ly
            bz = 0<=obj.z and obj.z <= self.lz

            L = 0<=obj.x + obj.larg and obj.x + obj.larg <= self.lx
            l = 0<=obj.y + obj.long and obj.y + obj.long <= self.ly
            h = 0<=obj.z + obj.haut and obj.z + obj.haut <= self.lx
        
            if bx and by and bz and L and l and h:
                self.cubes.append(obj)
                return True
            return False
        if isinstance(obj, Balise):
            self.balises.append(balises)

    
    def afficher(self):

        """Methode d'affichage d'une arene au format :
        Arene(limiteX= , limiteY= , limiteZ= )
        Liste d'objet [    ,    ,    ]
        """
        print("-------------------------------------------------\nArene(limiteX=%.2f,limiteY=%.2f,limiteZ=%.2f)"
              %(self.lx, self.ly, self.lz))
        print("LISTE OBJET\n[")
        for i in self.cubes:
            print(i.safficher())
        print("]")
        print("LISTE ROBOT\n[")
        for j in self.robots:
            print("\t"+j.safficher())
        print("]\n-------------------------------------------------")

    def retourne_angle(self,x,y,xx,yy) :
        """ retourne un angle teta en radian selon une direction initale d'un
            vecteur u(x,y) et une les coordonées du vecteur de la prochaine
            direction d'un vecteur v(xx,yy) en paramètres """

        sgn = (x*yy)+(xx*y)
        u = sqrt((x*x)+(y*y)) #norme de u
        v = sqrt((xx*xx)+(yy*yy)) #norme de v
        
        tmp = ((x*xx)+(y*yy))/(u+v)
        teta = acos(tmp)

        if(sgn < 0):
            return -1*teta
        return teta
    
def Creation_Arene() :
    lx = ARENE_LONGUEUR
    ly = ARENE_LARGEUR
    lz = ARENE_HAUTEUR # valeurs limites de l'arène
    arene = Arene(lx,ly,lz)
    arene.append(Cube(730+ROBOT_LONGUEUR, 15+ROBOT_LARGEUR, 0, 2, 20, 1))
    arene.append(Cube(0, 0, 0, 1, 1, 1))
    arene.append(Cube(0, 0, 0, 100, 100, 100))
    return arene