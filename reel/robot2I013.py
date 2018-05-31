# -*- coding: utf-8 -*-
import time
import math
from easygopigo3 import EasyGoPiGo3,Servo,DistanceSensor,MotionSensor
import picamera
from io import BytesIO
from PIL import Image
from di_sensors import distance_sensor as ds_sensor
from di_sensors import  inertial_measurement_unit as imu
from PIL import Image

class Robot2I013(object):
    """ 
    Classe d'encapsulation du robot et des senseurs.
    Constantes disponibles : 
    LED (controle des LEDs) :  LED_LEFT_EYE, LED_RIGHT_EYE, LED_LEFT_BLINKER, LED_RIGHT_BLINKER, LED_WIFI
    MOTEURS (gauche et droit) : MOTOR_LEFT, MOTOR_RIGHT
    et les constantes ci-dessous qui definissent les elements physiques du robot
    """

    WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
    WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
    WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi # perimetre du cercle de rotation (mm)
    WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi # perimetre de la roue (mm)
    
    def __init__(self,controler,fps=25,resolution=None,servoPort = "SERVO1",motionPort="AD1"):
        """ 
            Initialise le robot
            :controler: le controler du robot, muni d'une fonction update et d'une fonction stop qui 
                        rend in booleen (vrai a la fin du controle, faux sinon)
            :fps: nombre d'appel a controler.update() par seconde (approximatif!)
            :resolution: resolution de la camera
            :servoPort: port du servo (SERVO1 ou SERVO2)
            :motionPort: port pour l'accelerometre (AD1 ou AD2)
        """

        self._gpg= EasyGoPiGo3()
        self.controler = controler
        self.fps=fps
        self.LED_LEFT_EYE = self._gpg.LED_LEFT_EYE
        self.LED_RIGHT_EYE = self._gpg.LED_RIGHT_EYE
        self.LED_LEFT_BLINKER = self._gpg.LED_LEFT_BLINKER
        self.LED_RIGHT_BLINKER = self._gpg.LED_RIGHT_BLINKER
        self.LED_WIFI = self._gpg.LED_WIFI
        self.MOTOR_LEFT= self._gpg.MOTOR_LEFT
        self.MOTOR_RIGHT = self._gpg.MOTOR_RIGHT
        
        try:
            self.camera = picamera.PiCamera()
            if resolution:
                self.camera.resolution = resolution
        except Exception as e:
            print("Camera not found",e)
        try:
            self.servo = Servo(servoPort,self._gpg)
        except Exception as e:
            print("Servo not found",e)
        try:
            self.distanceSensor = ds_sensor.DistanceSensor()
        except Exception as e:
            print("Distance Sensor not found",e)
        try:
            self.imu = imu.InertialMeasurementUnit()
        except Exception as e:
            print("IMU sensor not found",e)
        self._gpg.set_motor_limits(self._gpg.MOTOR_LEFT+self._gpg.MOTOR_RIGHT,0)
#----------------------------------WRAPPER----------------------------------------
    def rotate(self, teta):
        self.set_motor_dps(self.MOTOR_LEFT, teta)
        self.set_motor_dps(self.MOTOR_RIGHT, -teta)

    def forward(self, speed):
        self.set_motor_dps(self.MOTOR_LEFT+self.MOTOR_RIGHT,speed)

    def curve(self, O, rayon):
        if(O == RIGHT):
            set_motor_dps(self.MOTOR_RIGHT, rayon)
            set_motor_dps(self.MOTOR_LEFT, rayon*2)
        else:
            set_motor_dps(self.MOTOR_RIGHT, rayon*2)
            set_motor_dps(self.MOTOR_LEFT, rayon)            

    def get_position(self):
        return self.get_motor_position()

    def get_image(self):
        stream = BytesIO()
        self.camera.capture(stream,format="jpeg")
        stream.seek(0)
        img= Image.open(stream).copy()
        stream.close()
        return img
    
    def dist_image(self, img1):
        """ retourne la distance entre deux images """
        
        img = self.getimage()
        width, height = img.size
        img2 = img.crop((x, y, larg, haut))
        img2 = img.resize((width, height))
        distance = 0

        for i in range(width):
            for j in range(height):
                r1, g1, b1 = img1.getpixel((i, j))
                r2, g2, b2 = img.getpixel((i, j))
                distance += ((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)

        return distance

    def save_image(self, cpt):
        img = self.getimage()
        imgpil = Image.fromarray(img)
        imgpil.save("tmp/img{0}.jpeg".format(cpt))
        
    def distance(self, last, current):
        lastRight, LastLeft = last
        currentRight, currentLeft = current
        return math.fabs(currentRight-lastRight)*self.WHEEL_CIRCUMFERENCE/360

    def isRed(self, color):
        ecart = 30
        r,g,b = color
        return r>=b and b>=g and r-b>ecart

    def isGreen(self, color):
        ecart = 30
        r,g,b = color
        return g>=r and r>=b and g-r>ecart

    def isBlue(self, color):
        ecart = 30
        r,g,b = color
        return b>=g and g>=r and b-g>ecart
      
    def isYellow(self, color):
        ecart = 30
        r,g,b = color
        return math.fabs(r-g)<=20 and (r-b>ecart or g-b>ecart)

    def isColor(self,color):
        ecart = 10
        r,g,b = color
        return not (math.fabs(r-g)<=ecart and math.fabs(g-b)<=ecart and math.fabs(r-b)<=ecart)

    def detecter_balise(self, img):
        dist = 20
        fenetre = (dist,dist)
        img = Image.open("reel/"+img)
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
                        if('r' in list_couleur and self.isRed(k)and self.isColor(list_coin[iter])):
                            list_couleur.remove('r')
                            #print('rouge')
                            img.putpixel((i,j), (255,108,0))
                        if('g' in list_couleur and self.isGreen(k)and self.isColor(list_coin[iter])):
                            list_couleur.remove('g')
                            #print('green')
                            img.putpixel((i,j), (0,177,100))
                        if('b' in list_couleur and self.isBlue(k)and self.isColor(list_coin[iter])):
                            list_couleur.remove('b')
                            #print('blue')
                            img.putpixel((i,j), (210,0,255))
                        if('y' in list_couleur and self.isYellow(k)and self.isColor(list_coin[iter])):
                            list_couleur.remove('y')
                            #print('yellow')
                            img.putpixel((i,j), (255,255,255))
                        """else:
                            print('rien')
                            img.putpixel((i,j), (184,177,171))"""
                        iter += 1
                    if(len(list_couleur) == 1):
                        print("Cible trouvée: pixel:",i,j)
                        #print("(r,g,b)",r1,g1,b1)
                        for x in range(dist):
                            for y in range(dist):
                                img.putpixel((i+x,j+y),(255,0,255))
                                
                        #img.show()
                        #img.close()

                        return (True,(i,j))
                j+=dist/2
            i+=dist/2
        #img.show()
#--------------------------------------------------------------------------------
    def run(self,verbose=True):
        """ 
            Boucle principale du robot. Elle appelle controler.update() fps fois par seconde 
            et s'arrete quand controler.stop() rend vrai.
            :verbose: booleen pour afficher les messages de debuggages
        """
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
        #    print("Erreur : ",e)
        self.stop()
        if verbose:
            print("Stoping ... total duration : %f (%f /loop)" % (time.time()-tstart,(time.time()-tstart)/cpt))

    def set_led(self, led, red = 0, green = 0, blue = 0):
        """
        Allume une led.
        
        :led: une des constantes LEDs (ou plusieurs combines avec +) : LED_LEFT_EYE, LED_RIGHT_EYE, LED_LEFT_BLINKER, LED_RIGHT_BLINKER, LED_WIFI.
        :red: composante rouge (0-255)
        :green:  composante verte (0-255)
        :blue: composante bleu (0-255)
        """
        self._gpg.set_led(led,red,green,blue)

    def get_voltage(self):
        """ get the battery voltage """
        return self._gpg.get_voltage_battery()


    def set_motor_dps(self, port, dps):
        """
        Fixe la vitesse d'un moteur en nombre de degres par seconde
        :port: une constante moteur,  MOTOR_LEFT ou MOTOR_RIGHT (ou les deux MOTOR_LEFT+MOTOR_RIGHT).
        :dps: la vitesse cible en nombre de degres par seconde
        """
        self._gpg.set_motor_dps(port,dps)
        self.set_motor_limits(port,dps)

    def set_motor_limits(self,port,dps):
        """
        Fixe la limite de la vitesse pour les moteurs (utile lorsqu'on utilise set_motor_position)
        
        :port: une constante moteur,  MOTOR_LEFT ou MOTOR_RIGHT (ou les deux MOTOR_LEFT+MOTOR_RIGHT).
        :dps: La vitesse limite en degres par seconde (0 pas de limite)
        """
        self._gpg.set_motor_limits(port,dps=dps)


    def get_motor_position(self):
        """
        Lit les etats des moteurs en degre.
        :return: couple du  degre de rotation des moteurs
        """
        return self._gpg.read_encoders()

    def set_motor_position(self, port, position):
        """
        Fixe la position des moteurs en degre.
        
        :port: un des deux moteurs MOTOR_LEFT ou MOTOR_RIGHT (ou les deux avec +).
        :position: la position cible en degre
        """
        self._gpg.set_motor_position(port,position)
    
    def offset_motor_encoder(self, port, offset):
        """
        Fixe l'offset des moteurs (en degres) (permet par exemple de reinitialiser a 0 l'etat 
        du moteur gauche avec offset_motor_encode(self.MOTOR_LEFT,self.read_encoders()[0])
        
        :port: un des deux moteurs MOTOR_LEFT ou MOTOR_RIGHT (ou les deux avec +)
        :offset: l'offset de decalage en degre.
        Zero the encoder by offsetting it by the current position
        """
        self._gpg.offset_motor_encoder(port,offset)

    def get_distance(self):
        """
        Lit le capteur de distance (en mm).
        :returns: entier distance en millimetre.
            1. L'intervalle est de **5-8,000** millimeters.
            2. Lorsque la valeur est en dehors de l'intervalle, le retour est **8190**.
        """
        return self.distanceSensor.read_range_single(False)

    def servo_rotate(self,position):
        """
        Tourne le servo a l'angle en parametre.
        :param int position: Angle de rotation, de **0** a **180** degres, 90 pour le milieu.
        """
        self.servo.rotate_servo(position)

    def stop(self):
        """ Arrete le robot """
        self.set_motor_dps(self.MOTOR_LEFT+self.MOTOR_RIGHT,0)
        self.set_led(self.LED_LEFT_BLINKER+self.LED_LEFT_EYE+self.LED_LEFT_BLINKER+self.LED_RIGHT_EYE+self.LED_WIFI,0,0,0)

def Creation_Robot(controler):
    return Robot2I013(controler)