

import glfw
from OpenGL.GL import * 
from OpenGL.GLU import * 
import numpy as np

T = np.array([[1., 0., 0.,0.], 
    [0., 1., 0.,0.],
    [0., 0., 1.,0.],
    [0., 0., 0.,1.]])
camAng= 0.

def render(M, canAng): 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    # draw cooridnate
    glOrtho(-1,1,-1,1,-1,1)
    gluLookAt(.1*np.sin(camAng),.1,.1*np.cos(camAng), 0,0,0, 0,1,0)

    glBegin(GL_LINES) 
    glColor3ub(255, 0, 0) 
    glVertex3fv(np.array([0.,0.,0.])) 
    glVertex3fv(np.array([1.,0.,0.])) 
    glColor3ub(0, 255, 0) 
    glVertex3fv(np.array([0.,0.,0.])) 
    glVertex3fv(np.array([0.,1.,0.])) 
    glColor3ub(0, 0, 255) 
    glVertex3fv(np.array([0.,0.,0.])) 
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
    # draw triangle
    glMultMatrixf(M.T)
    drawTriangle()

def drawTriangle(): 
	glColor3ub(255, 255, 255)
	glBegin(GL_TRIANGLES) 
	glVertex3fv(np.array([.0,.5,0.])) 
	glVertex3fv(np.array([.0,.0,0.])) 
	glVertex3fv(np.array([.5,.0,0.])) 
	glEnd()

def key_callback(window, key, scancode, action, mods):
    
    global T, camAng
    if action == glfw.PRESS:

        if key == glfw.KEY_Q:
            newArr = np.array([[1., 0.,0., -0.1],
                [0., 1., 0.,0.],
                [0., 0., 1.,0.],
                [0., 0., 0.,1.]])
            T = newArr@ T
        
        if key ==glfw.KEY_E:
            newArr = np.array([[1., 0.,0., 0.1],
                [0., 1., 0.,0.],
                [0., 0., 1.,0.],
                [0., 0., 0.,1.]])
            T = newArr@ T
        
        if key == glfw.KEY_A:
            newArr = np.array([[1., 0.,0., 0.],
                [0., 1., 0.,0.],
                [0., 0., 1.,0.],
                [0., 0., 0.,1.]])
            th=np.radians(-10)
            newArr[0][0]=np.cos(th)
            newArr[0][2]=np.sin(th)
            newArr[2][0]=-np.sin(th)
            newArr[2][2]=np.cos(th)
            T = T @ newArr
        
        if key ==glfw.KEY_D:
            newArr = np.array([[1., 0.,0., 0.],
                [0., 1., 0.,0.],
                [0., 0., 1.,0.],
                [0., 0., 0.,1.]])
            th=np.radians(10)
            newArr[0][0]=np.cos(th)
            newArr[0][2]=np.sin(th)
            newArr[2][0]=-np.sin(th)
            newArr[2][2]=np.cos(th)
            T = T @ newArr
        
        if key ==glfw.KEY_W:
            newArr = np.array([[1., 0.,0., 0.],
                [0., 1., 0.,0.],
                [0., 0., 1.,0.],
                [0., 0., 0.,1.]])
            th=np.radians(-10)
            newArr[1][1]=np.cos(th)
            newArr[1][2]=-np.sin(th)
            newArr[2][1]=np.sin(th)
            newArr[2][2]=np.cos(th)
            T = T @ newArr

        if key ==glfw.KEY_S:
            newArr = np.array([[1., 0.,0., 0.],
                [0., 1., 0.,0.],
                [0., 0., 1.,0.],
                [0., 0., 0.,1.]])
            th=np.radians(10)
            newArr[1][1]=np.cos(th)
            newArr[1][2]=-np.sin(th)
            newArr[2][1]=np.sin(th)
            newArr[2][2]=np.cos(th)
            T = T @ newArr

        if key == glfw.KEY_1:
            camAng-=np.radians(10)
            return 
        if key == glfw.KEY_3:
            camAng+=np.radians(10)
            return 



def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016026026", None,None)
    if not window: 
        glfw.terminate() 
        return new
    
    global T, camAng
    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events() 
        render(T, camAng)
        glfw.swap_buffers(window)
   
    glfw.terminate()


if __name__ == "__main__": 
    main()

