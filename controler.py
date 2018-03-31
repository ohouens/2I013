# -*- coding: utf-8 -*-
#from reel.robot2I013 import Robot2I013
from simulation.structures.robot import Robot
from simulation.structures.robot import Creation_Robot
from simulation.vues.vue2d import Vue2D
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
        self.etat = 1
        self.distance = 0
        self.vue = Vue2D(self)

    def update(self):
    #etat: 0=initialisation, 1=droit_70, 2=rotation à gauche, 3=carre
        print('Etat: {0}'.format(self.etat))
        self.currentPosition = self.robot.get_position()
        if(self.etat == 0):
            print("rien")
        if(self.etat == 1):
            self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 0, 255)
            self.robot.forward(300)
            self.distance += self.robot.distance(self.lastPosition, self.currentPosition)
            print("{0} > {1}\n".format(self.distance, 700-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))))
            if(self.distance > 700-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))):
                self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 255, 255)
                if(self.distance >= 700):
                    self.robot.stop()
                    self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 0)
                    self.distance = 0
                    self.etat = 2
                    #self.stop = True
                else:
                    self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 255)
                    self.robot.forward(20)
        if(self.etat == 2):
            print("on tourne")
            self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 255, 0)
            self.robot.rotate(100)
            self.distance += self.robot.distance(self.lastPosition, self.currentPosition)
            print("{0} > {1}\n".format(self.distance, math.pi*(self.robot.WHEEL_DIAMETER/1.5)/4))
            if(self.distance>math.pi*(self.robot.WHEEL_DIAMETER/1.5)/4):
                self.robot.stop()
                self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 0)
                self.distance = 0
                self.etat = 1
                #self.stop = True
        if(self.etat == 45):
            self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 255)
            self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 0, 255)
        self.lastPosition = self.currentPosition
    def stop(self):
        return self.stop
    def run(self):
        self.robot.run()

if __name__=="__main__":
    ctrl = TestControler()
    ctrl.run()
