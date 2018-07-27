

import glfw
from OpenGL.GL import * 
import numpy as np

T = np.array([[1., 0., 0.], 
    [0., 1., 0.],
    [0., 0., 1.]])

def render(T): 
    glClear(GL_COLOR_BUFFER_BIT) 
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES) 
    glColor3ub(255, 0, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([1.,0.])) 
    glColor3ub(0, 255, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.])) 
    glEnd()
    # draw triangle

    glBegin(GL_TRIANGLES)
    glColor3ub(255,255, 255)
    glVertex2fv((T @ np.array([.0,.5, 1.]))[:-1])
    glVertex2fv((T @ np.array([.0,.0, 1.]))[:-1])
    glVertex2fv((T @ np.array([.5,.0, 1.]))[:-1])
    glEnd()

def key_callback(window, key, scancode, action, mods):
    
    global T
    if action == glfw.PRESS:

        if key == glfw.KEY_Q:
            newArr = np.array([[1., 0., -0.1],
                [0., 1., 0.],
                [0., 0., 1.]])
            T = newArr@ T
        
        if key ==glfw.KEY_E:
            newArr = np.array([[1., 0., 0.1],
                [0., 1., 0.],
                [0., 0., 1.]])
            T = newArr@ T
        
        if key == glfw.KEY_A:
            newArr = np.array([[1., 0., 0.],
                [0., 1., 0.],
                [0., 0., 1.]])
            th=np.radians(10)
            newArr[0][0]=np.cos(th)
            newArr[0][1]=-np.sin(th)
            newArr[1][0]=np.sin(th)
            newArr[1][1]=np.cos(th)
            T = T @ newArr
        
        if key ==glfw.KEY_D:
            newArr = np.array([[1., 0., 0.],
                [0., 1., 0.],
                [0., 0., 1.]])
            th=np.radians(-10)
            newArr[0][0]=np.cos(th)
            newArr[0][1]=-np.sin(th)
            newArr[1][0]=np.sin(th)
            newArr[1][1]=np.cos(th)
            T = T @ newArr
        
        
        if key == glfw.KEY_1:
            T = np.array([[1., 0., 0.], 
                [0., 1., 0.],
                [0., 0., 1.]])
            return 


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016026026", None,None)
    if not window: 
        glfw.terminate() 
        return new
    
    global T
    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events() 
        render(T)
        glfw.swap_buffers(window)
   
    glfw.terminate()


if __name__ == "__main__": 
    main()

