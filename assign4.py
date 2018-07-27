import glfw
import math
import numpy as np
from OpenGL.GL import *

def f():
        global vertex
        vertex= np.arange(0,math.radians(360),math.radians(30))

def render():
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_LINE_LOOP)
        f()
        for x in vertex:
                glVertex2fv((np.cos(x), np.sin(x)))
        glEnd()

def key_callback(window, key, scancode, action, mods):
        if action ==glfw.PRESS:
                glFlush()
                glClear(GL_COLOR_BUFFER_BIT)ac
                glLoadIdentity()

                if key==glfw.KEY_1: 
                        glBegin(GL_POINTS)
                elif key==glfw.KEY_2:
                        glBegin(GL_LINES)
                elif key==glfw.KEY_3:
                        glBegin(GL_LINE_STRIP)
                elif key==glfw.KEY_4:
                        glBegin(GL_LINE_LOOP)
                elif key==glfw.KEY_5:
                        glBegin(GL_TRIANGLES)
                elif key==glfw.KEY_6:
                        glBegin(GL_TRIANGLE_STRIP)
                elif key==glfw.KEY_7:
                        glBegin(GL_TRIANGLE_FAN)
                elif key==glfw.KEY_8:
                        glBegin(GL_QUADS)
                elif key==glfw.KEY_9:
                        glBegin(GL_QUAD_STRIP)
                elif key==glfw.KEY_0:
                        glBegin(GL_POLYGON)
                f()
                for x in vertex:
                        glVertex2fv((np.cos(x),np.sin(x)))
                glEnd()
                glfw.swap_buffers(window)

def main():
# Initialize the library
        if not glfw.init():
                return
# Create a windowed mode window and its OpenGL context
        window = glfw.create_window(480,480,"Hello World", None,None)
        if not window:
                glfw.terminate()
                return


        glfw.set_key_callback(window, key_callback)
        glfw.make_context_current(window)
        render()   
        glfw.swap_buffers(window)
        while not glfw.window_should_close(window): # Poll events
                #glfw.swap_buffers(window)
                glfw.poll_events()
        glfw.terminate()

if __name__ == "__main__":
        main()
