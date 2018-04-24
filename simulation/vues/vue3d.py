# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import sys

display = (400,400)

class Vue3D:
	def __init__(self, controler):
		self.window = 0
		self.width = 200
		self.height = 200
		self.controler = controler
		self.robot = controler.robot
		self.width = self.robot.arene.lx
		self.height = self.robot.arene.ly

		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		glutInitWindowSize(display[0], display[1])
		glutInitWindowPosition(0, 0)
		glutCreateWindow(b"Simulation") 
		gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
		glTranslatef(0.0,0.0, -5)
		glutDisplayFunc(self.draw)
		glutIdleFunc(self.draw)
		glutMainLoop()

	def echelle(self, num):
		return num//700

	def draw_arene(self):
		for cube in self.robot.arene.cubes:
			self.draw_cube(cube.getCoords())
		#for balise in self.robot.arene.balises:
		#	self.draw_quad(balise.getCoords())

	def draw_cube(self, coords):
		p1, p2, p3, p4 =  coords
		verticies=(
			(p1[0], 0, p1[1]),
			(p2[0], 0, p2[1]),
			(p3[0], 0, p3[1]),
			(p4[0], 0, p4[1]),
			(p1[0], 1, p1[1]),
			(p2[0], 1, p2[1]),
			(p3[0], 1, p3[1]),
			(p4[0], 1, p4[1]),
		)
		edges=(
			(0,1),
			(0,3),
			(0,4),
			(2,1),
			(2,3),
			(2,6),
			(6,5),
			(6,7),
			(5,1),
			(5,4),
			(7,3),
			(7,4)
		)
		colors = (
    		(1,0,0),
    		(0,1,0),
    		(0,0,1),
    		(0,1,0),
    		(1,1,1),
    		(0,1,1),
    		(1,0,0),
    		(0,1,0),
    		(0,0,1),
    		(1,0,0),
    		(1,1,1),
    		(0,1,1),
    	)
		surfaces = (
    		(0,1,2,3),
    		(1,5,6,2),
    		(5,6,7,4),
    		(4,7,3,0),
    		(0,1,5,4),
    		(3,2,6,7)
    	)
		x = 0
		glBegin(GL_QUADS)
		for surface in surfaces:
			x+=1
			for vertex in surface:
				glColor3fv(colors[x])
				glVertex3fv(verticies[vertex])
		glEnd()
		glBegin(GL_LINES)
		for edge in edges:
			for vertex in edge:
				glVertex3fv(verticies[vertex])
		glEnd()

	def draw_quad(self, coords):
		p1,p2,p3,p4 = coords

	def draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		#glLoadIdentity()

		self.draw_arene()
		glRotatef(1,0,self.robot.getRotation(),0)
		glTranslatef(0,0,self.robot.getVitesse())	

		glutSwapBuffers()
		self.controler.update()
		time.sleep(1./25)