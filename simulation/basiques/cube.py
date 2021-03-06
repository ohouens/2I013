# -*- coding: utf-8 -*-
import random

class Cube():
    """Classe definissant un cube caractérisé par :
    - ses coordonnées, x, y, z
    - sa largueur
    - sa longueur
    - sa hauteur"""

    def __init__(self, x, y, z, larg, long, haut):
        """constructeur de la classe cube

        exemple de creation d'un cube : c1 = Cube(0,0,0,10,10,10)
        (création d'un cube de coordonnées x = y = z = 0 et de taille 10
        """
        self.x = x
        self.y = y
        self.z = z
        self.larg = larg
        self.long = long
        self.haut = haut
        
    def safficher(self):
        """Methode d'affichage d'un cube au format :
        cube[x= , y= , z= , larg= , long= , haut= ]
        """
        print("Cube(x=",self.x,",y=",self.y,",z=",self.z,", larg=",self.larg,",long=",self.long,",haut=",self.haut,")")

    def getPosition(self):
        return self.x, self.y, self.z

    def getDimension(self):
        return self.larg, self.long, self.haut

    def getCoords(self):
        p1 = self.x, self.y, self.z
        p2 = self.x+self.larg, self.y, self.z
        p3 = self.x+self.larg, self.y+self.long, self.z
        p4 = self.x, self.y+self.long, self.z
        return p1, p2, p3, p4