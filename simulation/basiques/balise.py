# -*- coding: utf-8 -*-
import random

class Balise(Cube):
    """Classe héritant de la classe Cube, caractérisée par:
        -ses coordonnées: x, y, z
        -sa hauteur
        -sa largueur
        -sa longueur"""

    def __init__(self, x, y, z):
        """Constructeur de la classe Mur"""
        Cube.__init__(self,x,y,z,5,300,200)

    def safficher(self):
        """Methode d'affichage d'un mur au format :
        mur[x= , y= , z= , larg= , long= , haut= ]
        """
        print("balise(x=%.2f,y=%.2f,z=%.2f, larg=%.2f,long=%.2f,haut=%.2f)"%(self.x, self.y, self.z, self.larg, self.long, self.haut))