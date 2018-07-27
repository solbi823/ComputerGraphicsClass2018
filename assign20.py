import glfw
from OpenGL.GL import *
from OpenGL.GLU import * 
import numpy as np
from OpenGL.arrays import vbo 
import ctypes

gCamAng = 0. 
gCamHeight = 1.
gAxis = np.array([0.,1.,0.]) 


def l2norm(v):
	return np.sqrt(np.dot(v, v))

def normalized(v): 
	l = l2norm(v)
	return 1/l * np.array(v)

def getRotMatFrom(axis, theta):

	normalizedAxis = normalized(axis)
	p = np.cross(normalizedAxis ,[0,0,1] )
	normalizedP = normalized(p)

	Ra = np.column_stack(([0,0,1], 
						normalizedP , 
						normalized(np.cross(p, [0,0,1]))
						))

	RbInversed = np.column_stack((normalizedAxis, 
								normalizedP, 
								normalized(np.cross(normalizedAxis, normalizedP))
								))

	Rb = np.linalg.inv(RbInversed)

	Raz = Ra@Rb
	RazInversed = np.linalg.inv(Raz)

	Rz = np.array([[np.cos(theta), -np.sin(theta), 0],
					[np.sin(theta), np.cos(theta), 0],
					[0, 0, 1]])

	return RazInversed@Rz@Raz

def createVertexAndIndexArrayIndexed(): 
	varr = np.array([
				normalized([1,1,-1]), 
				[ 0.5, 0.5,-0.5], 
				normalized([-1,1,-1]), 
				[-0.5, 0.5,-0.5], 
				normalized([-1,1,1]), 
				[-0.5, 0.5, 0.5], 
				normalized([1,1,1]), 
				[ 0.5, 0.5, 0.5], 
				normalized([1,-1,1]), 
				[ 0.5,-0.5, 0.5], 
				normalized([-1,-1,1]), 
				[-0.5,-0.5, 0.5], 
				normalized([-1,-1,-1]), 
				[-0.5,-0.5,-0.5], 
				normalized([1,-1,-1]), 
				[ 0.5,-0.5,-0.5],
				], 'float32') 

	iarr = np.array([[0,1,2], 
					[0,2,3], 
					[4,5,6], 
					[4,6,7], 
					[3,2,5], 
					[3,5,4], 
					[7,6,1], 
					[7,1,0], 
					[2,1,6], 
					[2,6,5], 
					[0,3,4], 
					[0,4,7], 
					])
	return varr, iarr

def drawUnitCube_glDrawElements():
	global gVertexArrayIndexed, gIndexArray 
	varr = gVertexArrayIndexed
	iarr = gIndexArray 
	glEnableClientState(GL_VERTEX_ARRAY) 
	glEnableClientState(GL_NORMAL_ARRAY) 
	glNormalPointer(GL_FLOAT, 6*varr.itemsize,varr)
	glVertexPointer(3, GL_FLOAT,
	6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
	glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)
	                                      

def createVertexArraySeparate(): 
	varr = np.array([
				[0,1,0],
				[ 0.5, 0.5,-0.5], 
				[0,1,0],
				[-0.5, 0.5,-0.5], 
				[0,1,0],
				[-0.5, 0.5, 0.5],
				[0,1,0],
				[ 0.5, 0.5,-0.5], 
				[0,1,0],
				[-0.5, 0.5, 0.5], 
				[0,1,0],
				[ 0.5, 0.5, 0.5],
				[0,-1,0],
				[ 0.5,-0.5, 0.5], 
				[0,-1,0], 
				[-0.5,-0.5, 0.5], 
				[0,-1,0], 
				[-0.5,-0.5,-0.5],
				[0,-1,0],
				[ 0.5,-0.5, 0.5], 
				[0,-1,0], 
				[-0.5,-0.5,-0.5], 
				[0,-1,0],
				[ 0.5,-0.5,-0.5],
				[0,0,1],
				[ 0.5, 0.5, 0.5], 
				[0,0,1],
				[-0.5, 0.5, 0.5], 
				[0,0,1], 
				[-0.5,-0.5, 0.5],
				[0,0,1],
				[ 0.5, 0.5, 0.5], 
				[0,0,1], 
				[-0.5,-0.5, 0.5], 
				[0,0,1],
				[ 0.5,-0.5, 0.5],   

				[0,0,-1],
				[ 0.5,-0.5,-0.5], 
				[0,0,-1], 
				[-0.5,-0.5,-0.5], 
				[0,0,-1],
				[-0.5, 0.5,-0.5],
				[0,0,-1],
				[ 0.5,-0.5,-0.5], 
				[0,0,-1],
				[-0.5, 0.5,-0.5], 
				[0,0,-1],
				[ 0.5, 0.5,-0.5],
				[-1,0,0],
				[-0.5, 0.5, 0.5], 
				[-1,0,0],
				[-0.5, 0.5,-0.5], 
				[-1,0,0], 
				[-0.5,-0.5,-0.5],
				[-1,0,0],
				[-0.5, 0.5, 0.5], 
				[-1,0,0], 
				[-0.5,-0.5,-0.5], 
				[-1,0,0], 
				[-0.5,-0.5, 0.5],
				[1,0,0],
				[ 0.5, 0.5,-0.5], 
				[1,0,0],
				[ 0.5, 0.5, 0.5], 
				[1,0,0],
				[ 0.5,-0.5, 0.5],
				[1,0,0],
				[ 0.5, 0.5,-0.5], 
				[1,0,0],
				[ 0.5,-0.5, 0.5], 
				[1,0,0],
				[ 0.5,-0.5,-0.5], 
				], 'float32')

	return varr       


def render(ang):

	global gCamAng, gCamHeight
	global gAxis 

	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glEnable(GL_DEPTH_TEST)

	glMatrixMode(GL_PROJECTION) 
	glLoadIdentity() 
	gluPerspective(45, 1, 1,10)

	glMatrixMode(GL_MODELVIEW) 
	glLoadIdentity()
	gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

	drawFrame() # draw global frame

	    # draw rotation axis
	glBegin(GL_LINES)
	glColor3ub(255, 255, 255) 
	glVertex3fv(np.array([0.,0.,0.])) 
	glVertex3fv(gAxis)
	glEnd()

	glEnable(GL_LIGHTING) 
	glEnable(GL_LIGHT0) 
	glEnable(GL_RESCALE_NORMAL)

	glLightfv(GL_LIGHT0, GL_POSITION, (1.,2.,3.,1.))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (.1,.1,.1,1.)) 
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.,1.,1.,1.)) 
	glLightfv(GL_LIGHT0, GL_SPECULAR, (1.,1.,1.,1.))


	 # for your answer
	R = getRotMatFrom(gAxis, ang) 
	M = np.identity(4)
	M[:3,:3] = R 
	glMultMatrixf(M.T)
	    # # for debugging - your result should be samewith the result from this glRotate() call
	    # glRotatef(ang, gAxis[0], gAxis[1], gAxis[2])
	glScalef(.5,.5,.5)
	# draw cubes
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (.5,.5,.5,1.))
	drawUnitCube_glDrawArray()
	glTranslatef(1.5,0,0)
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.,0.,0.,1.))
	drawUnitCube_glDrawArray()
	glTranslatef(-1.5,1.5,0)
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0.,1.,0.,1.))
	drawUnitCube_glDrawArray()
	glTranslatef(0,-1.5,1.5)
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0.,0.,1.,1.))
	drawUnitCube_glDrawArray() 
	glDisable(GL_LIGHTING)


def drawUnitCube_glDrawArray():
	global gVertexArraySeparate
	varr = gVertexArraySeparate 
	glEnableClientState(GL_VERTEX_ARRAY) 
	glEnableClientState(GL_NORMAL_ARRAY) 
	glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr) 
	glVertexPointer(3, GL_FLOAT, 6*varr.itemsize,
	ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize)) 
	glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))


def drawFrame():
	glBegin(GL_LINES)
	glColor3ub(255, 0, 0) 
	glVertex3fv(np.array([0.,0.,0.])) 
	glVertex3fv(np.array([1.,0.,0.])) 
	glColor3ub(0, 255, 0) 
	glVertex3fv(np.array([0.,0.,0.])) 
	glVertex3fv(np.array([0.,1.,0.])) 
	glColor3ub(0, 0, 255) 
	glVertex3fv(np.array([0.,0.,0])) 
	glVertex3fv(np.array([0.,0.,1.])) 
	glEnd()


def key_callback(window, key, scancode, action, mods):

	global gAxis

	if action==glfw.PRESS or action==glfw.REPEAT:
		if key==glfw.KEY_A: 
			gAxis[0] += 0.1
		elif key==glfw.KEY_Z: 
			gAxis[0] -= 0.1
		elif key==glfw.KEY_S: 
			gAxis[1] += 0.1
		elif key==glfw.KEY_X: 
			gAxis[1] -= 0.1
		elif key==glfw.KEY_D: 
			gAxis[2] += 0.1
		elif key==glfw.KEY_C:
			gAxis[2] -= 0.1
		elif key==glfw.KEY_V: 
			gAxis[0] = 0
			gAxis[1] = 1
			gAxis[2] = 0



gVertexArraySeparate = None 
gVertexArrayIndexed = None 
gIndexArray = None

def main():
	global gVertexArraySeparate
	global gVertexArrayIndexed, gIndexArray
	global gAxis

	angle = 0.

	if not glfw.init(): 
		return
	window = glfw.create_window(640,640,'2016026026', None,None) 
	if not window:
		glfw.terminate()
		return
	glfw.make_context_current(window) 
	glfw.set_key_callback(window, key_callback)
	glfw.swap_interval(1)

	gVertexArraySeparate = createVertexArraySeparate() 
	gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

	while not glfw.window_should_close(window):
		glfw.poll_events()
		angle += 0.02
		render(angle%360)
		glfw.swap_buffers(window)

	glfw.terminate()




if __name__ == "__main__": 
	main()
 