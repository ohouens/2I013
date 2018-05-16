# -*- coding: utf-8 -*-
#from reel.robot2I013 import Robot2I013
from simulation.structures.robot import Robot
from simulation.structures.robot import Creation_Robot
from simulation.vues.vue2d import Vue2D
from simulation.vues.vue3d import Vue3D
from cste import *
import time
import numpy as np
import math

class TestControler(object):
    def __init__(self):
        """ Initialise le controleur et un robot """
        self.robot = Creation_Robot(self)
        self.stop = False
        self.lastPosition = self.robot.get_position()
        self.currentPosition = self.robot.get_position()
        #strategie 0=exit, 1=droit 70cm, 2=rotation 90°, 3=carre, 4=cercle, 5=séries de photos, 6=detection de balise, 7=suivi de balise, 8=double cercle
        self.strategie = 8
        self.tour = 0
        self.temoin = False 
        self.distance = 0
        self.cpt = 1
        self.save = 0
        self.vue = Vue2D(self)

    def droit(self, D):
        """
            Avance tout droit jusqu'a une certaine distance D
            D en mm
        """
        self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 0, 255)
        self.robot.forward(300)
        self.distance += self.robot.distance(self.lastPosition, self.currentPosition)
        print("{0} > {1}\n".format(self.distance, D-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))))
        if(self.distance > D-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))):
            self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 255, 255)
            if(self.distance >= D):
                self.robot.stop()
                self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 0)
                self.distance = 0
                return True
            else:
                self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 255)
                self.robot.forward(45)
              
    def arriere(self, D):
        self.robot.forward(-100)
        self.distance += self.robot.distance(self.lastPosition, self.currentPosition)
        print("{0} > {1}\n".format(self.distance, D-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))))
        if(self.distance > D-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))):
            if(self.distance >= D):
                self.robot.stop()
                self.distance = 0
                return True
            else:
                self.robot.forward(-25)

    def rotation(self, O, D):
        """
            Tourne vers un sens de rotation O jusqu'a un certain angle D
            D en degré
        """
        self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 255, 0)
        sens = 300
        if(O == RIGHT):
            sens = sens*(RIGHT)
        self.robot.rotate(sens)
        self.distance += self.robot.distance(self.lastPosition, self.currentPosition)
        print("{0} > {1}\n".format(self.distance, math.pi*(self.robot.WHEEL_DIAMETER*0.4)/(360/D)))
        if(self.distance > math.pi*(self.robot.WHEEL_DIAMETER*0.4)/(360/D)):
                self.robot.stop()
                self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 0)
                self.distance = 0
                return True

    def courbe(self, O, D):
        """
            Effectue une courbe vers un sens de rotation O jusqu'a une certaine distance D
            D en mm
        """
        self.robot.curve(O, 50)
        self.distance += self.robot.distance(self.lastPosition, self.currentPosition)
        print("{0} > {1}".format(self.distance, math.pi*(self.robot.WHEEL_CIRCUMFERENCE)*D))
        if(self.distance > math.pi*(self.robot.WHEEL_CIRCUMFERENCE)*D):
            self.robot.stop()
            self.distance = 0
            return True

    def initialisation(self):
        """
            Vérifie les éléments du robot
        """
        self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 255)
        self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 0, 255)

    def update(self):
        print('\nStratégie: {0}'.format(self.strategie))
        self.currentPosition = self.robot.get_position()
        if(self.robot.get_distance() <= 100):
            self.save = self.strategie
            self.strategie = 403
        if(self.strategie == 0):
            self.robot.stop()
            exit(0)
        elif(self.strategie == 1):
            if(self.droit(700)):
                self.strategie = 0
        elif(self.strategie == 2):
            if(self.rotation(LEFT, 90)):
                self.strategie = 0
        elif(self.strategie == 3):
            if(self.tour < 4):
                if(not self.temoin):
                    if(self.droit(700)):
                        self.temoin = True
                else:
                    if(self.rotation(LEFT, 90)):
                        self.temoin = False
                        self.tour += 1
            else:
                self.strategie = 0
        elif(self.strategie == 4):
            if(self.courbe(LEFT, 1.2)):
                self.strategie = 0
        elif(self.strategie == 5):
            if(not self.droit(700)):
                if(self.cpt %10 == 0):
                    self.robot.save_image(self.cpt/10)
            else:
                self.strategie = 0
            self.cpt += 1
        elif(self.strategie == 6):
            print("photo")
            self.robot.detecter_balise("simulation/tmp/img1.jpeg")
            self.strategie = 0
        elif(self.strategie == 7):
            if(self.cpt %10 == 0):
                self.robot.save_image(self.cpt/10)
                detecte, cible = self.robot.detecter_balise("simulation/tmp/img{0}.jpeg".format(self.cpt/10))
                if (detecte):
                    if (cible[0]<IMG_WIDTH/3):
                        self.rotation(LEFT,20)
                    if (cible[0]>2*IMG_WIDTH/3):
                        self.rotation(RIGHT,20)
                    else: 
                        self.droit(50)
            #else:
                #self.strategie = 0
            self.cpt += 1
        elif(self.strategie == 8):
            if(self.temoin):
                if(self.courbe(RIGHT, 1.02)):
                    self.temoin = False
            else:
                if(self.courbe(LEFT, 1.2)):
                    self.temoin = True
        elif(self.strategie == 403):
            self.robot.stop()
            print('stop')
            if(self.robot.get_distance() > 100):
                self.strategie = self.save
        else:
            print("rien")
        self.lastPosition = self.currentPosition
        
    def run(self):
        self.robot.run()

if __name__=="__main__":
    ctrl = TestControler()
    ctrl.run()
