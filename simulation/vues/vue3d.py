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
		glutDisplayFunc(self.draw)
		glutIdleFunc(self.draw)
		glutMainLoop()

	def draw_arene(self):
		for cube in self.robot.arene.cubes:
			self.draw_cube(cube.getCoords(), cube.haut)
		for balise in self.robot.arene.balises:
			x, y = balise
			p1 = (x, y)
			p2 = (x+3, y)
			p3 = (x+3, y+2)
			p4 = (x, y+2)
			self.draw_quad((p1, p2, p3, p4))

	def draw_cube(self, coords, height):
		p1, p2, p3, p4 =  coords
		verticies=(
			(p1[0], 0, p1[1]),
			(p2[0], 0, p2[1]),
			(p3[0], 0, p3[1]),
			(p4[0], 0, p4[1]),
			(p1[0], height, p1[1]),
			(p2[0], height, p2[1]),
			(p3[0], height, p3[1]),
			(p4[0], height, p4[1]),
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
		
		glBegin(GL_LINES)
		for edge in edges:
			for vertex in edge:
				glVertex3fv(verticies[vertex])
		glEnd()

	def draw_quad(self,):
		x = 0
		glBegin(GL_QUADS)
		for surface in surfaces:
			x+=1
			for vertex in surface:
				glColor3fv(colors[x])
				glVertex3fv(verticies[vertex])
		glEnd()

	def draw_balise(self, coords, height):
		p1,p2,p3,p4 = coords
		verticies = (
			(p1[0], 			0, 			p1[1]),				#0
			((p1[0]+p2[0])/2, 	0, 			(p1[1]+p2[1])/2),	#1
			(p2[0], 			0, 			p2[1]),				#2
			(p2[0], 			height/2, 	p2[1]),				#3
			(p2[0], 			height, 	p2[1]),				#4
			((p1[0]+p2[0])/2, 	height, 	(p1[1]+p2[1])/2),	#5
			(p1[0], 			height, 	p1[1]),				#6
			(p1[0], 			height/2, 	p1[1]),				#7
			((p1[0]+p2[0])/2, 	height/2, 	(p1[1]+p2[1])/2)	#8
		)
		surfaces = (
			(0, 1, 8, 7),
			(1, 2, 3, 8),
			(8, 3, 4, 5),
			(7, 8, 5, 6)
		)
		draw_quad(verticies, surfaces, colors)

	def refresh3d(self):
		glViewport(0, 0, self.width, self.height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
		glMatrixMode (GL_MODELVIEW)
		glLoadIdentity()

	def draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		refresh3d()

		self.draw_arene()

		glutSwapBuffers()
		self.controler.update()
		time.sleep(1./25)