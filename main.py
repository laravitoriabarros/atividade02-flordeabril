# -*- coding: utf-8 -*-
# Flor de abril: 4 pétalas triangulares + cabinho
# Controles: P (play/pause), R (reset), ESC (sair)
# Requisitos: pip install PyOpenGL PyOpenGL_accelerate

from math import cos, sin, pi
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# ---------------- Configs visuais ----------------
R_PETALA = 0.28         # comprimento da pétala (raio)
ABERTURA = pi/6         # "largura" angular de cada triângulo (meia-abertura)
CENTRO_Y = -0.10        # posição vertical da flor (negativo = mais baixo)
HASTE_LEN = 0.60        # comprimento do cabo
HASTE_LARG = 6.0        # espessura da linha do cabo
FUNDO = (0.0, 0.0, 0.0) # cor de fundo
CORES = [
    (1.0, 0.0, 0.0),  # vermelho
    (0.0, 1.0, 0.0),  # verde
    (0.0, 0.0, 1.0),  # azul
    (1.0, 1.0, 0.0),  # amarelo
]

# ---------------- Estado ----------------
angle = 0.0
rotating = False
speed = 120.0           # graus/segundo

def tri_petal(base_angle):
    """
    Desenha UMA pétala triangular com vértice no centro (0,0)
    e os outros dois vértices na circunferência em (base±ABERTURA).
    """
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

    # move para baixo para parecer com a referência
    glTranslatef(0.0, CENTRO_Y, 0.0)

    # desenha haste (traço) a partir do centro para baixo
    glLineWidth(HASTE_LARG)
    glColor3f(0.95, 0.88, 0.75)  # bege clarinho
    glBegin(GL_LINES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, -HASTE_LEN)
    glEnd()

    # gira o conjunto das pétalas
    glPushMatrix()
    glRotatef(angle, 0, 0, 1)

    # pétalas nas direções 45°, 135°, 225°, 315° (pinwheel)
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
    elif key == b'\x1b':  # ESC
        glutLeaveMainLoop()

def timer(_):
    global angle
    if rotating:
        dt = 1.0/60.0
        # Sentido horário (direita)
        angle = (angle - speed*dt) % 360.0
        glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = w / float(max(h, 1))
    # mantém a proporção em coordenadas -1..1
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
    glutInitWindowSize(700, 1000)  # janela mais "alta", como no print
    glutCreateWindow(b"Flor de Abril - P: girar/pausar | R: reset | ESC: sair")
    init_gl()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
