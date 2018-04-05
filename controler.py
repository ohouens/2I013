# -*- coding: utf-8 -*-
from reel.robot2I013 import Robot2I013
#from simulation.structures.robot import Robot
#from simulation.structures.robot import Creation_Robot
#from simulation.vues.vue2d import Vue2D
import time
import numpy as np
import math
class TestControler(object):
    def __init__(self):
        """ Initialise le controleur et un robot """
        self.robot = Robot2I013(self,25)
        self.stop = False
        self.lastPosition = self.robot.get_position()
        self.currentPosition = self.robot.get_position()
        self.strategie = 0
        self.etat = 2
        self.tour = 0
        self.distance = 0
        #self.vue = Vue2D(self)
        self.cpt=0

    def update(self):
    #strategie 0=exit, 3=carre, 4=cercle, 5=séries de photos
    #etat: 0=initialisation, 1=droit_70, 2=rotation à gauche, 3=courbe à gauche, 4=photo
        print('Etat: {0}'.format(self.etat))
        self.currentPosition = self.robot.get_position()
        if(self.etat == 0):
            if(self.strategie == 0):
                self.robot.stop()
                self.stop()
                exit(0)
            elif(self.strategie == 1):
                self.tour = 0
                self.etat = 2
            elif(self.strategie == 3):
                if(self.tour < 4):
                    self.etat = 2
                else:
                    self.strategie = 0
            elif(self.strategie == 4):
                self.etat = 3
            elif(self.strategie == 5):
                self.etat = 1
            else:
                print("rien")
        elif(self.etat == 1):
            self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 0, 255)
            self.robot.forward(300)
            self.distance += self.robot.distance(self.lastPosition, self.currentPosition)
            #self.etat = 4
            print("{0} > {1}\n".format(self.distance, 700-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))))
            if(self.distance > 700-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))):
                self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 255, 255)
                if(self.distance >= 700):
                    self.robot.stop()
                    self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 0)
                    self.distance = 0
                    self.etat = 0
                    #self.stop = True
                else:
                    self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 255)
                    self.robot.forward(45)
        elif(self.etat == 2):
            print("on tourne")
            self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 255, 0)
            self.robot.rotate(300)
            self.distance += self.robot.distance(self.lastPosition, self.currentPosition)
            print("{0} > {1}\n".format(self.distance, math.pi*(self.robot.WHEEL_DIAMETER)/4))
            if(self.distance>math.pi*(self.robot.WHEEL_DIAMETER)/4):
                self.robot.stop()
                self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 0)
                self.distance = 0
                self.tour += 1
                self.etat = 0
                #self.stop = True
        elif(self.etat == 3):
            self.robot.forward(50)
            self.robot.rotate(50)
        elif(self.etat == 4):
            if(self.cpt%250):
                self.robot.save_image(self.cpt)
            self.cpt+=1
            self.etat=1
        elif(self.etat == 45):
            self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 255)
            self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 0, 255)
        else:
            print('rien')
        self.lastPosition = self.currentPosition
        
    def stop(self):
        return self.stop
    def run(self):
        self.robot.run()

if __name__=="__main__":
    ctrl = TestControler()
    ctrl.run()