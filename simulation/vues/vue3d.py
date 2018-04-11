# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import sys

class Vue3D:
	def __init__(self, controler):
		self.window = 0
		self.width = 200
		self.height = 200
		self.controler = controler
		self.robot = controler.robot
		self.width = self.robot.arene.lx
		self.height = self.robot.arene.ly