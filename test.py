from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

window = 0
width = 400
height = 400

r_x = 10
r_y = 10

larg = 200
haut = 100
def move(limite_x, limite_y):
	global r_x
	global r_y
	if(r_x +larg < limite_x and r_y == 0):
		r_x += 1
	elif(r_y+haut < limite_y and r_x+larg >= limite_x):
		r_y += 1
	elif(r_x > 0 and r_y+haut == limite_y):
		r_x -= 1
	else:
		r_y -= 1


def draw_rect(x, y, width, height):
	glBegin(GL_QUADS)
	glVertex2f(x, y)
	glVertex2f(x + width, y)
	glVertex2f(x + width, y + height)
	glVertex2f(x, y + height)
	glEnd()

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	refresh2d(width, height)

	glColor3f(1.0, 0.0, 1.0)
	move(width, height)
	draw_rect(r_x, r_y, larg, haut)

	glutSwapBuffers()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"fenetre")
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutMainLoop()