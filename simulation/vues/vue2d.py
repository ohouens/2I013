# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import sys

class Vue2D:
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
		glutInitWindowSize(self.width, self.height)
		glutInitWindowPosition(0, 0)
		glutCreateWindow(b"Simulation")
		glutDisplayFunc(self.draw)
		glutIdleFunc(self.draw)
		glutMainLoop()

	def draw_arene(self):
		for cube in self.robot.arene.cubes:
			self.draw_quad(cube.getCoords())

	def draw_robot(self):
		p1, p2, p3, p4 = self.robot.getCoords()
		self.draw_quad(self.robot.getCoords())
		#self.draw_quad(self.robot.leftWheel().getCoords())
		#self.draw_quad(self.robot.rightWheel().getCoords())
		#self.draw_quad(self.robot.head().getCoords())


	def draw_quad(self, coords):
		p1,p2, p3, p4 = coords
		glBegin(GL_QUADS)
		glVertex2f(p1[0], p1[1])
		glVertex2f(p2[0], p2[1])
		glVertex2f(p3[0], p3[1])
		glVertex2f(p4[0], p4[1])
		glEnd()	

	def refresh2d(self):
		glViewport(0, 0, self.width, self.height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
		glMatrixMode (GL_MODELVIEW)
		glLoadIdentity()

	def draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		self.refresh2d()

		glColor3f(1.0, 0.0, 1.0)
		self.draw_arene()
		glColor3f(0.0, 0.3, 1.0)
		self.draw_robot()

		glutSwapBuffers()
		self.controler.update()
		time.sleep(1./self.robot.fps)
