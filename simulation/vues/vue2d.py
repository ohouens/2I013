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
			self.draw_rect(cube.getPosition(), cube.getDimension())

	def draw_robot(self):
		self.draw_rect(self.robot.getPosition(), self.robot.getDimension())

	def draw_rect(self, position, dimension):
		x, y, z = position
		longu, larg, haut = dimension
		glBegin(GL_QUADS)
		glVertex2f(x, y)
		glVertex2f(x + longu, y)
		glVertex2f(x + longu, y + larg)
		glVertex2f(x, y + larg)
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
