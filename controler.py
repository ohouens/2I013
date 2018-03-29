# -*- coding: utf-8 -*-
#from reel.robot2I013 import Robot2I013
from simulation.structures.robot import Robot
from simulation.structures.robot import Creation_Robot
import time
import numpy as np
import math
class TestControler(object):
    def __init__(self):
        """ Initialise le controleur et un robot """
        self.robot = Creation_Robot(self)
        self.cpt = 0
        self.moteur_pos = 1
        self.etat = 45
        self.distance = 1

    def update(self):
    #etat: 0=initialisation, 1=droit_70, 2=rotation à gauche, 3=carre
        print('update')
        print("{0} >>> {1}".format(self.distance, 700-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))))
        moteur_g, moteur_d = self.robot.get_position()
        if(self.etat == 0):
            print("rien")
        if(self.etat == 1):
            self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 0, 255)
            self.robot.forward(300)
            self.distance += (math.fabs(moteur_g - self.moteur_pos)/360)*math.pi*self.robot.WHEEL_DIAMETER
            print("{0} > {1}".format(self.distance, 700-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))))
            if(self.distance > 700-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))):
                self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 255, 255)
                if(self.distance >= 700):
                    self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 0)
                    self.robot.stop()
                    self.moteur_pos = 1
                    self.distance = 1
                    self.etat = 2
                else:
                    self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 255)
                    self.robot.forward(20)
            self.moteur_pos = moteur_g;
        if(self.etat == 2):
            print("on tourne")
            self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 255, 0)
            self.robot.rotate(300)
            self.distance += ((moteur_g - self.moteur_pos)/360)*math.pi*self.robot.WHEEL_DIAMETER
            if(self.distance>math.pi*(self.robot.WHEEL_DIAMETER/2)):
                self.robot.stop()
                self.etat = 1
        if(self.etat == 45):
            self.robot.set_led(self.robot.LED_LEFT_EYE, 0, 255, 255)
            self.robot.set_led(self.robot.LED_RIGHT_EYE, 255, 0, 255)
    def stop(self):
        return self.cpt>80
    def run(self):
        self.robot.run()

if __name__=="__main__":
    ctrl = TestControler()
    ctrl.run()
