# -*- coding: utf-8 -*-
from robot2I013 import Robot2I013
import time
import numpy as np
import math
class TestControler(object):
    def __init__(self, robot):
        """ Initialise le controleur et un robot """
        self.robot = robot(Creation_Robot(self))
        self.cpt = 0
        self.moteur_pos = 1
        self.etat = 1
        self.distance = 1
    def set_led(self,col):
        """ Allume les leds du robot au triplet col=(r,g,b) """
        self.robot.set_led(self.robot.LED_LEFT_EYE+self.robot.LED_RIGHT_EYE,*col)
    def set_speed(self,lspeed,rspeed):
        """ Fait tourner les moteurs a la vitesse lspeed pour le moteur gauche, rspeed pour le moteur droit """
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT,lspeed)
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT,rspeed)
    def forward(self,speed):
        """ Avant le robot a la vitesse speed """
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT+self.robot.MOTOR_RIGHT,speed)


    def update(self):
    #etat: 0=initialisation, 1=droit_70, 2=rotation à gauche, 3=carre
        print('update')
        print("{0} >>> {1}".format(self.distance, 700-(2*math.pi*(self.robot.WHEEL_DIAMETER/2))))
        moteur_g, moteur_d = self.robot.get_motor_position()
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
            self.robot.set_speed(-300, 300)
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