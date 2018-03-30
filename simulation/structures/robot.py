import random
import math
import time
from simulation.structures.teteRobot import TeteRobot
from simulation.structures.teteRobot import Creation_TeteRobot
from simulation.structures.arene import Arene
from simulation.structures.arene import Creation_Arene
class Robot:
    """
        Classe caractérisé par:
        Sa Position: triplet(x, y, z)
        Les coordonnees de ses 4 angles (xy0, xy1, xy2, xy3)
        Sa direction: triplet(a, b)
        Sa dimension(final): triplet(longueur, largeur, hauteur)
        Sa vitesse: entier
        sa tete: Class TeteRobot
    """

    WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
    WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
    WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi # perimetre du cercle de rotation (mm)
    WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi # perimetre de la roue (mm)

    def __init__(self, position, coords, direction, dimension, vitesse, controler=None, fps=25):
    	self.controler = controler
    	self.position = position
    	self.coords = coords
    	self.direction = direction
    	self.dimension = dimension
    	self.vitesse = vitesse
    	self.tete = Creation_TeteRobot()
    	self.arene = Creation_Arene()
    	self.fps = fps

    	self.LED_LEFT_EYE = "LED_LEFT_EYE"
    	self.LED_RIGHT_EYE = "LED_RIGHT_EYE"
    	self.LED_LEFT_BLINKER = "LED_LEFT_BLINKER"
    	self.LED_RIGHT_BLINKER = "LED_RIGHT_BLINKER"
    	self.LED_WIFI = "LED_WIFI"
    	self.MOTOR_LEFT= "MOTOR_LEFT"
    	self.MOTOR_RIGHT = "MOTOR_RIGHT"
#----------------------------------WRAPPER----------------------------------------
    def rotate(self, teta):
        self.rotation_bis(teta)
        print(self.toString())

    def forward(self, speed):
        self.setVitesse(speed)
        print(self.toString())

    def stop(self):
        self.setVitesse(0)
        print(self.toString())

    def set_led(self, led, r, g, b):
        print("LED: {0}, color({1}, {2}, {3})".format(led, r, g, b))

    def get_position(self):
    	self.move_bis()
    	x, y, z = self.getPosition()
    	#print("x: {0}, y:{1}".format(x, y))
    	return x, y

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
#--------------------z------------------------------------------------------------
    def move_bis(self):
        x, y, z = self.position
        xdir, ydir = self.direction
        #larg, long, haut = self.dimension
        (x0,y0), (x1,y1), (x2,y2), (x3,y3) = self.coords
        
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
        (x0,y0), (x1,y1), (x2,y2), (x3,y3) = self.coords
        
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
        #print("coords=",self.coords)
        self.calcdir()              #maj direction du robot
        

    def calcdir(self):
        """ Calcule la direction du robot (correspond a l'avant du robot) et retourne cette derniere sous la forme : (x, y) """
        (x0,y0), (x1,y1), (x2,y2), (x3,y3) = self.coords

        dirxy1 = (self.position[0], self.position[1])
        dirxy2 = ( ((x0 + x1)/2), ((y0+y1)/2) )
        newdir = ( (dirxy2[0]-dirxy1[0]), (dirxy2[1]-dirxy1[1]) )
        self.__setDirection(newdir)

    
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

    """-----------------------SETTER-------------------------"""
    def __setPosition(self, position):
        self.position = position

    def __setDirection(self, direction):
        self.direction = direction

    def setVitesse(self, vitesse):
        self.vitesse = vitesse

    def setCoords(self, coords):
        self.coords = coords
        
        
    
    """-----------------------SAVER-------------------------"""
    def toSaveF(self, f):
        """Ecrit les coordonnees du robot dans le fichier ouvert passe en argument, avec ';' comme separation"""
        f.write('Robot;' + str(self.position) + ';' +  str(self.direction) + ';' + str(self.dimension) + ';' + str(self.vitesse) + ';\n')

        

def Creation_Robot(controler):
	position = (0,15,0)
	coordonnees = ((0,0),(0,0),(0,0),(0,0))
	direction = (1,0)
	dimension = (25, 10, 15)
	vitesse = (10)
	return Robot(position, coordonnees, direction, dimension, vitesse, controler)