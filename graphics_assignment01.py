import glfw
from OpenGL.GL import * 
from OpenGL.GLU import * 
import numpy as np

gCamAng = np.radians(45)

def render(camAng, count): 
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glPolygonMode( GL_FRONT_AND_BACK, GL_LINE ) 
	glEnable(GL_DEPTH_TEST)
	glLoadIdentity()

# use orthogonal projection (multiply the current matrix by "projection" matrix - we'll see details later)
	glOrtho(-1,1, -1,1, -1,1)
# rotate "camera" position (multiply the current matrix by "camera" matrix - we'll see details later)
	gluLookAt(0.1*np.sin(camAng),-0.3,0.1*np.cos(camAng), 0,-0.35,0, 0,1,0)


	countTemp= count%180

	if(countTemp>90):
		countTemp= 180-countTemp

	count1 = countTemp-150
	count2 = -60-(countTemp)
	
	#drawFrame()

	######################## head and body part
	
	# body transformation
	glPushMatrix() 
	glRotatef((countTemp-45)/2, 0, 1, 0)
	# body drawing
	glPushMatrix()
	glScalef(.2, .3, .2) 
	glColor3ub(206, 238, 242) 
	drawSphere()
	glPopMatrix()

	glPushMatrix()
	glTranslatef(0, .45, 0)
	glScalef(.15, .15, .15) 
	glColor3ub(206, 238, 242) 
	drawSphere()
	glPopMatrix()

	######################## arms part

    # right arm high part transformation 
	glPushMatrix() 
	glRotatef(count1, 0, 0, 1) 
	glTranslatef(.08, 0., .2)
    # right arm high part drawing
	glPushMatrix() 
	glScalef(.2, .02, .02) 
	glColor3ub(72, 171, 205) 
	drawCube()
	glPopMatrix()

	# right arm low part transformation
	glPushMatrix()
	glTranslatef(0.2, 0, 0)
	glRotatef(210+count1, 0,.15,1)
	glTranslatef(0.2, 0, 0)
	# right arm low part drawing
	glPushMatrix()
	glScalef(.2, .02, .02)
	glColor3ub(72, 171, 205)
	drawCube()
	glPopMatrix()

	# right hand part transformation and drawing.
	glPushMatrix()
	glTranslatef(0.2, 0, 0)
	glScalef(.07, .05, .02) 
	glColor3ub(72, 171, 205) 
	drawSphere()
	glPopMatrix()

	glPopMatrix()
	glPopMatrix() 

	# left arm high part transformation
	glPushMatrix() 
	glRotatef(count2, 0, 0, 1) 
	glTranslatef(.08, 0., -0.2)
    # left arm high part drawing
	glPushMatrix() 
	glScalef(.2, .02, .02) 
	glColor3ub(72, 171, 205)
	drawCube()
	glPopMatrix()

	# left arm low part transformation
	glPushMatrix()
	glTranslatef(0.2, 0, 0)
	glRotatef(210+count2, 0,-0.15,1)
	glTranslatef(0.2, 0, 0)
	# left arm low part drawing
	glPushMatrix()
	glScalef(.2, .02, .02)
	glColor3ub(72, 171, 205)
	drawCube()
	glPopMatrix()

	# left hand part transformation and drawing.
	glPushMatrix()
	glTranslatef(0.2, 0, 0)
	glScalef(.07, .05, .02) 
	glColor3ub(72, 171, 205) 
	drawSphere()
	glPopMatrix()

	glPopMatrix()
	glPopMatrix()

	######################## legs part

	# right leg high part transformation 
	glPushMatrix() 
	glRotatef(count2*0.6-25, 0 , 0.05 , 1) 
	glTranslatef(0.5, 0., .08)
    # right leg high part drawing
	glPushMatrix() 
	glScalef(.25, .02, .02) 
	glColor3ub(43, 136, 135) 
	drawCube()
	glPopMatrix()

	# right leg low part transformation
	glPushMatrix()
	glTranslatef(0.25, 0, 0)
	glRotatef(count2*1.1+75, 0,-0.2,1)
	glTranslatef(0.25, 0, 0)
	# right leg low part drawing
	glPushMatrix()
	glScalef(.25, .02, .02)
	glColor3ub(43, 136, 135)
	drawCube()
	glPopMatrix()

	# right foot part transformation and drawing.
	glPushMatrix()
	glTranslatef(0.3, 0.06, 0)
	glRotatef(count2*0.8+70, 0,0.2,1)
	glScalef(.035, .13, .06) 
	glColor3ub(43, 136, 135)
	drawSphere()
	glPopMatrix()

	glPopMatrix()
	glPopMatrix() 



	# left leg high part transformation 
	glPushMatrix() 
	glRotatef(count1*0.6-25, 0 , -0.05 , 1) 
	glTranslatef(0.5, 0.,-0.08)
    # left leg high part drawing
	glPushMatrix() 
	glScalef(.25, .02, .02) 
	glColor3ub(43, 136, 135) 
	drawCube()
	glPopMatrix()

	# left leg low part transformation
	glPushMatrix()
	glTranslatef(0.25, 0, 0)
	glRotatef(count1*1.1+75, 0,0.2,1)
	glTranslatef(0.25, 0, 0)
	# left leg low part drawing
	glPushMatrix()
	glScalef(.25, .02, .02)
	glColor3ub(43, 136, 135)
	drawCube()
	glPopMatrix()

	# left foot part transformation and drawing.
	glPushMatrix()
	glTranslatef(0.3, 0.06, 0)
	glRotatef(count1*0.8+70, 0,0.2,1)
	glScalef(.035, .13, .06) 
	glColor3ub(43, 136, 135)
	drawSphere()
	glPopMatrix()

	glPopMatrix()
	glPopMatrix() 


	glPopMatrix()



 # draw a cube of side 2, centered at the origin.
def drawCube():
	glBegin(GL_QUADS)

	glVertex3f( 1.0, 1.0,-1.0) 
	glVertex3f(-1.0, 1.0,-1.0) 
	glVertex3f(-1.0, 1.0, 1.0)
	glVertex3f( 1.0, 1.0, 1.0)

	glVertex3f( 1.0,-1.0, 1.0) 
	glVertex3f(-1.0,-1.0, 1.0)
	glVertex3f(-1.0,-1.0,-1.0)
	glVertex3f( 1.0,-1.0,-1.0)

	glVertex3f( 1.0, 1.0, 1.0)
	glVertex3f(-1.0, 1.0, 1.0) 
	glVertex3f(-1.0,-1.0, 1.0) 
	glVertex3f( 1.0,-1.0, 1.0)

	glVertex3f( 1.0,-1.0,-1.0) 
	glVertex3f(-1.0,-1.0,-1.0) 
	glVertex3f(-1.0, 1.0,-1.0) 
	glVertex3f( 1.0, 1.0,-1.0)

	glVertex3f(-1.0, 1.0, 1.0)
	glVertex3f(-1.0, 1.0,-1.0)
	glVertex3f(-1.0,-1.0,-1.0) 
	glVertex3f(-1.0,-1.0, 1.0)

	glVertex3f( 1.0, 1.0,-1.0)
	glVertex3f( 1.0, 1.0, 1.0) 
	glVertex3f( 1.0,-1.0, 1.0) 
	glVertex3f( 1.0,-1.0,-1.0)

	glEnd()
	 


# draw a sphere of radius 1, centered at the origin.
# numLats: number of latitude segments (horizontal)
# numLongs: number of longitude segments (horizontal)
def drawSphere(numLats=24, numLongs=24):

	for i in range(0, numLats + 1):

		lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
		z0 = np.sin(lat0)
		zr0 = np.cos(lat0)
		lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
		z1 = np.sin(lat1)
		zr1 = np.cos(lat1)

		# Use Quad strips to draw the sphere
		glBegin(GL_QUAD_STRIP)

		for j in range(0, numLongs + 1):

			lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
			x = np.cos(lng) 
			y = np.sin(lng)
			glVertex3f(x * zr0, y * zr0, z0) 
			glVertex3f(x * zr1, y * zr1, z1)

		glEnd()
	 

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


def drawTriangle(): 
	glColor3ub(255,255,255)
	glBegin(GL_TRIANGLES) 
	glVertex3fv(np.array([.0,.5,0.])) 
	glVertex3fv(np.array([.0,.0,0.])) 
	glVertex3fv(np.array([.5,.0,0.])) 
	glEnd()

def key_callback(window, key, scancode, action, mods):
	global gCamAng
    # rotate the camera when 1 or 3 key is pressed or repeated
	if action==glfw.PRESS or action==glfw.REPEAT: 
		if key==glfw.KEY_1:
			gCamAng += np.radians(-10) 
		elif key==glfw.KEY_3:
			gCamAng += np.radians(10)

def main():
	if not glfw.init():
		return
	window = glfw.create_window(640,640,'Running girl', None,None)
	if not window: 
		glfw.terminate()
		return
	glfw.make_context_current(window) 
	glfw.set_key_callback(window, key_callback)
	glfw.swap_interval(1)

	count=0
	while not glfw.window_should_close(window): 
		glfw.poll_events()
		render(gCamAng,count) 
		glfw.swap_buffers(window)
		count+=5

	glfw.terminate()

if __name__ == "__main__": 
	main()
