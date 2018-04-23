from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import time

display=(400,400)

verticies=(
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
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

ground_surfaces = (0,1,2,3)

ground_vertices = (
    (-10,-0.1,50),
    (10,-0.1,50),
    (-10,-0.1,-300),
    (10,-0.1,-300),
    )

def Ground():
    
    glBegin(GL_QUADS)

    x = 0
    for vertex in ground_vertices:
        x+=1
        glColor3fv((0,1,1))
        glVertex3fv(vertex)
        
    glEnd()

def Cube():
    x = 0
    glBegin(GL_QUADS)
    for surface in surfaces:
        #x = 0
        x+=1
        for vertex in surface:
            #x+=1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	#glLoadIdentity()
	glRotatef(1,0,1,0)
	#glTranslatef(0,0,-1)
	#refresh3d(width, height)
	#Ground()
	Cube()
	time.sleep(1./25)

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