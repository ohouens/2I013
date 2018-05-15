# -*- coding: utf-8 -*-
import random
import math
import time
from cste import *
from simulation.structures.teteRobot import TeteRobot
from simulation.structures.teteRobot import Creation_TeteRobot
from simulation.structures.arene import Arene
from simulation.structures.arene import Creation_Arene
#from PIL import ImageGrab
import pyscreenshot as ImageGrab
from PIL import Image

class Robot:
    """
        Classe caractérisé par:
        Sa Position: triplet(x, y, z)
        Les coordonnees de ses 4 angles (xy0, xy1, xy2, xy3)
        Sa direction: doublet(a, b)
        Sa dimension(final): triplet(longueur, largeur, hauteur)
        Sa vitesse: entier
        Sa rotation: entier
        sa tete: Class TeteRobot
    """

    WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
    WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
    WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi # perimetre du cercle de rotation (mm)
    WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi # perimetre de la roue (mm)

    def __init__(self, position, direction, dimension, vitesse, controler=None, fps=25):
        self.controler = controler
        self.position = position
        self.direction = direction
        self.dimension = dimension
        self.vitesse = vitesse
        self.rotation = 0
        self.tete = TeteRobot((1,0))
        self.arene = Creation_Arene()
        self.fps = fps

        p1 = (self.position[0]-ROBOT_LONGUEUR, self.position[1]-ROBOT_LARGEUR)
        p2 = (self.position[0]+ROBOT_LONGUEUR, self.position[1]-ROBOT_LARGEUR)
        p3 = (self.position[0]+ROBOT_LONGUEUR, self.position[1]+ROBOT_LARGEUR)
        p4 = (self.position[0]-ROBOT_LONGUEUR, self.position[1]+ROBOT_LARGEUR)
        self.coords = (p1, p2, p3, p4)

        self.LED_LEFT_EYE = "LED_LEFT_EYE"
        self.LED_RIGHT_EYE = "LED_RIGHT_EYE"
        self.LED_LEFT_BLINKER = "LED_LEFT_BLINKER"
        self.LED_RIGHT_BLINKER = "LED_RIGHT_BLINKER"
        self.LED_WIFI = "LED_WIFI"
        self.MOTOR_LEFT= "MOTOR_LEFT"
        self.MOTOR_RIGHT = "MOTOR_RIGHT"
        
#----------------------------------WRAPPER----------------------------------------
    def rotate(self, teta):
        self.rotation = teta
        self.rotation_bis(teta/10)
        print(self.toString())

    def forward(self, speed):
        self.setVitesse(speed)
        self.rotation = 0
        print(self.toString())

    def curve(self, O, rayon):
        if(O == RIGHT):
            rayon = rayon*RIGHT
        self.forward(100)
        self.rotate(rayon)

    def stop(self):
        self.setVitesse(0)
        #self.rotation = 0
        print(self.toString())

    def set_led(self, led, r, g, b):
        print("LED: {0}, color({1}, {2}, {3})".format(led, r, g, b))

    def get_position(self):
    	self.move_bis()
    	#x, y, z = self.getPosition()
    	#print("x: {0}, y:{1}".format(x, y))
    	p1, p2, p3, p4 = self.getCoords()
    	return p2[0], p2[1]

    def get_distance(self):
        p1, p2, p3, p4 = self.getCoords()
        vx, vy = self.tete.getOrientation()
        for i in range(0,10):
            a = (p1[0]+p2[0])/2 + i*vx
            b = (p1[1]+p2[1])/2 + i*vy
            print("({0}, {1})".format(a,b))
            if(self.tete.isCube((a, b, 0), self.arene.cubes)):
                return (math.sqrt(
                        ((p1[0]+p2[0])/2+i*vx - (p1[0]+p2[0])/2)**2 +
                        ((p1[1]+p2[1])/2+i*vy - (p1[1]+p2[1])/2)**2
                ))
        return 8190

    def distance(self, last, current):
    	x1, y1 = last
    	x2, y2 = current
    	print("x1: {0}, y1:{1}".format(x1, y1))
    	print("x2: {0}, y2:{1}".format(x2, y2))
    	print("distance: {0}".format(math.sqrt((x2-x1)**2+(y2-y1)**2)))
    	return math.sqrt((x2-x1)**2+(y2-y1)**2)

    def run(self,verbose=True):
    	if verbose:
    		print("Starting ... (with %f FPS  -- %f sleep)" % (self.fps,1./self.fps))
    	ts=time.time()
    	tstart = ts
    	cpt = 1
    	#try:
    	while not self.controler.stop:
    		ts = time.time()
    		self.controler.update()
    		time.sleep(1./self.fps)
    		if verbose:
    			print("Loop %d, duree : %fs " % (cpt,time.time()-ts))
    		cpt+=1
    	#except Exception as e:
    	#	print("Erreur : ",e)
    	self.stop()
    	if verbose:
        	print("Stoping ... total duration : %f (%f /loop)" % (time.time()-tstart,(time.time()-tstart)/cpt))

    def get_image(self):
        img = ImageGrab.grab()
        return img
        
    def dist_image(self, img1, img2):
        """ retourne la distance entre deux images """
        
        #img = self.getimage()
        img1= Image.open(img1)
        img2= Image.open(img2)

        width, height = img1.size
        #img2 = img1.crop((10, 10, width, height))
        #img2 = img2.resize((width, height))
        #img1 = img1.resize((width,height))
        distance = 0

        for i in range(width):
            for j in range(height):
                r1, g1, b1 = img1.getpixel((i, j))
                r2, g2, b2 = img2.getpixel((i, j))
                distance += ((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)
                print("distance:",distance)

        return distance

    def save_image(self, cpt):
        img = self.get_image()
        #imgpil = Image.open(img)
        #img = img.crop((0, 0, IMG_WIDTH, IMG_HEIGHT))
        img = img.resize((IMG_WIDTH, IMG_HEIGHT))
        img.save("simulation/tmp/img{0}.jpeg".format(cpt))
        print("simulation/tmp/img{0}.jpeg".format(cpt))

    def isRed(self, color):
        r,g,b = color
        #return r>=b and b>=g 
        return r>200 and b<20 and g<20
    def isGreen(self, color):
        r,g,b = color
        #return g>=r and r>=b 
        return g>200 and b<20 and r<20
    def isBlue(self, color):
        r,g,b = color
        #return b>=g and g>=r
        return b>200 and r<20 and g<20
      
    def isYellow(self, color):
        r,g,b = color
        #return math.fabs(r-g)<=20
        return r>200 and g>200 and b<20
    def isColor(self,color):
        r,g,b = color
        return math.fabs(r-g)>=10 and math.fabs(g-b)>=10

    def detecter_balise(self, img):
        dist = 20
        fenetre = (dist,dist)
        img = Image.open(img)
        width, height = img.size
        
        i = 0
        j = 0
       # cible = (0,0)
        while i<width-dist:
            j=0
            while j<height-dist:
                
                list_couleur = ['r','g','b','y']
                list_coin = [
                    img.getpixel((i,j)),
                    img.getpixel((i+dist,j)),
                    img.getpixel((i,j+dist)),
                    img.getpixel((i+dist,j+dist))
                ]
                #print("{0},{1}".format(i,j))
                cpt=0
                for k in list_coin:
                    r1, g1, b1 = k
                    iter = 0
                    while(iter < len(list_couleur)):
                        if('r' in list_couleur and self.isRed(k)): #and self.isColor(list_coin[iter])):
                            list_couleur.remove('r')
                            #print('rouge')
                            #img.putpixel((i,j), (255,108,0))
                        if('g' in list_couleur and self.isGreen(k)):#and self.isColor(list_coin[iter])):
                            list_couleur.remove('g')
                            #print('green')
                            #img.putpixel((i,j), (0,177,100))
                        if('b' in list_couleur and self.isBlue(k)):#and self.isColor(list_coin[iter])):
                            list_couleur.remove('b')
                            #print('blue')
                            #img.putpixel((i,j), (210,0,255))
                        if('y' in list_couleur and self.isYellow(k)):#and self.isColor(list_coin[iter])):
                            list_couleur.remove('y')
                            #print('yellow')
                            #img.putpixel((i,j), (255,255,255))
                        iter += 1
                    if(len(list_couleur) == 1):
                        print("Cible trouvée: pixel:",i,j)
                        #print("(r,g,b)",r1,g1,b1)
                        for x in range(dist):
                            for y in range(dist):
                                img.putpixel((i+x,j+y),(255,0,255))
                                
                        #img.show()

                        return (True,(i,j))
                j+=dist//2
            i+=dist//2
        #img.show()

        print("Pas de cible")
        return (False,(-1,-1))
#--------------------z------------------------------------------------------------
    def move_bis(self):
        x, y, z = self.position
        #larg, long, haut = self.dimension
        (x0,y0), (x1,y1), (x2,y2), (x3,y3) = self.coords
        xdir, ydir = self.direction
        
        vitesse = self.vitesse

        v0 = (self.direction[0]*vitesse)/10
        v1 = (self.direction[1]*vitesse)/10
        
        x += v0
        y += v1
        

        x0 += v0
        y0 += v1
        x1 += v0
        y1 += v1
        x2 += v0
        y2 += v1
        x3 += v0
        y3 += v1
        
        self.__setPosition((x, y, z))
        self.setCoords(((x0,y0),(x1,y1),(x2,y2),(x3,y3)))
        #print("dir=",self.direction,"    centre=",self.position,"    coords=",self.coords)
        
        
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


    def rotation_bis(self,teta):
        """Effectue une rotation du robot (sur lui-même) de teta°"""
        angle = math.radians(teta)
        x,y = self.getDirection()
        (x0,y0), (x1,y1), (x2,y2), (x3,y3) = self.coords
        
        newX = x*math.cos(angle) - y*math.sin(angle)
        newY = x*math.sin(angle) + y*math.cos(angle)
        self.__setDirection((newX, newY))

        ctx0 = (x0-self.position[0])*math.cos(angle) - (y0-self.position[1])*math.sin(angle) + self.position[0]
        cty0 = (x0-self.position[0])*math.sin(angle) + (y0-self.position[1])*math.cos(angle) + self.position[1]

        ctx1 = (x1-self.position[0])*math.cos(angle) - (y1-self.position[1])*math.sin(angle) + self.position[0]
        cty1 = (x1-self.position[0])*math.sin(angle) + (y1-self.position[1])*math.cos(angle) + self.position[1]
    
        ctx2 = (x2-self.position[0])*math.cos(angle) - (y2-self.position[1])*math.sin(angle) + self.position[0]
        cty2 = (x2-self.position[0])*math.sin(angle) + (y2-self.position[1])*math.cos(angle) + self.position[1]
    
        ctx3 = (x3-self.position[0])*math.cos(angle) - (y3-self.position[1])*math.sin(angle) + self.position[0]
        cty3 = (x3-self.position[0])*math.sin(angle) + (y3-self.position[1])*math.cos(angle) + self.position[1]

        newcoords = [ ((ctx0), (cty0)),
                      ((ctx1), (cty1)),
                      ((ctx2), (cty2)),
                      ((ctx3), (cty3))]
        
        self.setCoords(newcoords)   #maj coords des 4 points du robot

    def rotation_tete(self, teta):
        self.tete.rotation(teta)

    def toString(self):
        return "ROBOT[Corps]|position: {0}, direction: {1}, dimension{2}, vitesse: {3}".format(self.getPosition(),self.getDirection(),self.getDimension(),self.getVitesse())+"\n"+self.tete.toString()

    def safficher(self):
                """Methode d'affichage d'un robot au format :
                Robot[position, direction, taille, vitesse]
                """
                return "ROBOT([Corps] position: {0}, direction: {1}, dimension{2}, vitesse: {3}".format(self.getPosition(),self.getDirection(),self.getDimension(),self.getVitesse())#||| "+self.tete.safficher()+")"
                

    """-----------------------GETTTER-------------------------"""
    def getPosition(self):
        return self.position

    def getDirection(self):
        return self.direction

    def getDimension(self):
        return self.dimension

    def getVitesse(self):
        return self.vitesse

    def getRotation(self):
        return self.rotation

    def getCoords(self):
    	return self.coords

    """-----------------------SETTER-------------------------"""
    def __setPosition(self, position):
        self.position = position

    def __setDirection(self, direction):
        self.direction = direction

    def setVitesse(self, vitesse):
        self.vitesse = vitesse

    def setCoords(self, coords):
        self.coords = coords

def Creation_Robot(controler):
	position = (500,500,0)
	direction = (1,0)
	dimension = (ROBOT_LONGUEUR, ROBOT_LARGEUR, ROBOT_HAUTEUR)
	vitesse = (0)
	return Robot(position, direction, dimension, vitesse, controler)