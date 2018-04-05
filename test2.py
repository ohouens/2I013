from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

display=(400,400)

vertices=(
	(1, -1, -1),
	(1, 1, -1),
	(-1, 1, -1),
	(-1, -1, -1),
	(1, -1, 1),
	(1, 1, 1),
	(-1, -1, 1),
	(-1, 1, 1)
	)

edges=(
	(0,1),
	(0,3),
	(0,4),
	(2,1),
	(2,3),
	(2,7),
	(6,3),
	(6,4),
	(6,7),
	(5,1),
	(5,4),
	(5,7)
	)

def Cube():
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
	glEnd()

def refresh3d(width, height):
    glViewport(0, 0, display[0], display[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, display[0], 0.0, height, 0.0, display[1])
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw():
	#glRotatef(1,3,1,1)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	#glLoadIdentity()
	#refresh3d(width, height)

	glColor3f(1.0, 0.0, 1.0)
	Cube()

	glutSwapBuffers()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(display[0], display[1])
glutInitWindowPosition(0, 0)
glutCreateWindow(b"fenetre") 
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0,0.0, -5)
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutMainLoop()