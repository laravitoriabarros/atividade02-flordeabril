# Controles: P (iniciar/pausar), R (resetar/voltar a posição de inicio), ESC (sair)

#AVISO: INSTALE AS BIBLIOTECAS DO README PARA TUDO FUNCIONAR CORRETAMENTE
#QUALQUER DÚVIDA ENTRAR EM CONTATO: lvssb@ic.ufal.br

from math import cos, sin, pi
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

R_PETALA = 0.28
ABERTURA = pi/6
CENTRO_Y = -0.10
HASTE_LEN = 0.60
HASTE_LARG = 6.0
FUNDO = (0.0, 0.0, 0.0)
CORES = [
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0),
    (1.0, 1.0, 0.0),
]

angle = 0.0
rotating = False
speed = 120.0

def tri_petal(base_angle):
    a1 = base_angle - ABERTURA
    a2 = base_angle + ABERTURA
    x1, y1 = R_PETALA*cos(a1), R_PETALA*sin(a1)
    x2, y2 = R_PETALA*cos(a2), R_PETALA*sin(a2)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, CENTRO_Y, 0.0)
    glLineWidth(HASTE_LARG)
    glColor3f(0.95, 0.88, 0.75)
    glBegin(GL_LINES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, -HASTE_LEN)
    glEnd()
    glPushMatrix()
    glRotatef(angle, 0, 0, 1)
    bases = [pi/4, 3*pi/4, 5*pi/4, 7*pi/4]
    for i, b in enumerate(bases):
        glColor3f(*CORES[i])
        tri_petal(b)
    glPopMatrix()
    glutSwapBuffers()

def keyboard(key, x, y):
    global rotating, angle
    if key in (b'p', b'P'):
        rotating = not rotating
    elif key in (b'r', b'R'):
        angle = 0.0
        glutPostRedisplay()
    elif key == b'\x1b':
        glutLeaveMainLoop()

def timer(_):
    global angle
    if rotating:
        dt = 1.0/60.0
        angle = (angle - speed*dt) % 360.0
        glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = w / float(max(h, 1))
    if aspect >= 1.0:
        glOrtho(-1.2*aspect, 1.2*aspect, -1.2, 1.2, -1, 1)
    else:
        glOrtho(-1.2, 1.2, -1.2/aspect, 1.2/aspect, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init_gl():
    glClearColor(*FUNDO, 1.0)
    glDisable(GL_DEPTH_TEST)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(700, 1000)
    glutCreateWindow(b"Flor de Abril - P: girar/pausar | R: resetar | ESC: sair")
    init_gl()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
