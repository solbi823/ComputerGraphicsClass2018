# 2016026026 최솔비 
# 컴퓨터 그래픽스 과제 3: OBJ Viewer


import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes
import string
import sys
import os

gCamAng = 0.
gCamHeight = 2.
gCamZoom = 1.5
gPolygonFlag = 0

gVertexArray = None
gVertexNormalArray = None
gFaceArrays = None

gVertexArraySeparate = np.array([], 'float32')

# faceCount[number of vertices] = number of faces
faceCount = None
gTotalFace = 1


class FaceArray :
    vertexNumber = None
    faceArr = None
    triangleArr = None

    def __init__(self, vertexNumber):
        self.vertexNumber = vertexNumber

    def getFaceToArr(self, faceArr):
        self.faceArr = faceArr

    def makeTriangle(self):

        self.triangleArr = np.array([[0,0,0]], dtype = int )

        index = 0
        while len(self.faceArr) > index+2 :
            self.triangleArr = np.r_[self.triangleArr,[self.faceArr[0]]]
            self.triangleArr = np.r_[self.triangleArr,[self.faceArr[index+1]]]
            self.triangleArr = np.r_[self.triangleArr,[self.faceArr[index+2]]]
            index += 1

        self.triangleArr = np.delete(self.triangleArr, (0), axis = 0)

        return self.triangleArr




def render(ang):
    global gCamAng, gCamHeight, gCamZoom, gPolygonFlag
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    if gPolygonFlag == 1:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE ) 
    elif gPolygonFlag == 0:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION) # use projection matrix stack for projection transformation for correct lighting
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(gCamZoom* 5*np.sin(gCamAng), gCamZoom* gCamHeight, gCamZoom* 5*np.cos(gCamAng), 
                0,0,0, 
                0,1,0)

    drawFrame()

    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # light0 position
    glPushMatrix()

    lightPos = (1.,2.,3.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    glPopMatrix()

    # light1 position
    glPushMatrix()

    glRotatef(ang,0,1,0)  # light1 은 회전합니다. 
    lightPos = (2.,4.,6.,2.) 
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    glPopMatrix()



    # light intensity for each color channel
    ambientLightColor = (.05,.05,.05,1.)
    diffuseLightColor = (.5,.5,.5,1.)
    specularLightColor = (3.,3.,3.,1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLightColor)

    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, specularLightColor)

    # material reflectance for each color channel
    diffuseObjectColor = (1.,0.,0.,1.)
    specularObjectColor = (1.,0.,0.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, diffuseObjectColor)
    #glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    #glRotatef(ang,0,1,0)    # try to uncomment: rotate object

    glColor3ub(0, 0, 255) # glColor*() is ignored if lighting is enabled

    drawUnitCube_glDrawArray()
    glPopMatrix()

    glDisable(GL_LIGHTING)


def makeTriangle_createVertexArraySeperate():
    global gTotalFace, faceCount, gVertexArray, gVertexNormalArray, gFaceArrays
    global gTrianguler

    vTarr = np.array([[0.,0.,0.]], 'float32')

    for i in range(0, gTotalFace):
        tempArr = gFaceArrays[i].makeTriangle()

        for brr in tempArr:
            v = brr[0]
            vn = brr[2]
            vTarr = np.r_[vTarr, [gVertexNormalArray[vn]]]
            vTarr = np.r_[vTarr, [gVertexArray[v]]]


    vTarr = np.delete(vTarr, (0), axis = 0)

    return vTarr

    
def drawUnitCube_glDrawArray():

    varr = gVertexArraySeparate

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
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
    global gCamAng, gCamHeight, gCamZoom, gPolygonFlag
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

            #insert zoom in and zoom out function

        elif key==glfw.KEY_S:
            gCamZoom += .1
        elif key==glfw.KEY_A:
            gCamZoom += -.1

        elif key==glfw.KEY_Z:
            #wireframe // solid mode change
            gPolygonFlag = not gPolygonFlag



# read file and save data into data structure.
def read_and_print_file(paths):

    global gVertexArraySeparate
    global gTotalFace, faceCount, gVertexArray, gVertexNormalArray, gFaceArrays

    gTotalFace = 0                  # 이 오브젝트 파일이 몇개의 face를 가지고 있는지 셉니다. 

    f = open(paths[0], 'r')
    while True:
        line = f.readline()
        if not line : 
            break
        # get a line successfully

        line.rstrip('\n')
        lineArr = line.split(' ')
        if lineArr[0]=='o':
            objName = lineArr[1]

        elif lineArr[0]=='v':               #vertex
            tmpVertex = np.array([float(lineArr[1]), float(lineArr[2]), float(lineArr[3])], 'float32')
            gVertexArray = np.r_[gVertexArray, [tmpVertex]]

        elif lineArr[0]=='vn':              #vertex normal
            tmpNormal = np.array([float(lineArr[1]), float(lineArr[2]), float(lineArr[3])], 'float32')
            gVertexNormalArray = np.r_[gVertexNormalArray , [tmpNormal]]

        elif lineArr[0]=='f':               #face : vertex / texture coordinate / vertex normal

            tempCount = 0           #한 face안에 몇개의 vertex를 가지고 있는지 셉니다. 

            lineFaceArray = np.array([[0,0,0]], dtype = 'int')

            for i in lineArr:           
                if i =='f':
                    continue

                tempCount += 1
                tmpFace = i.split('/')
                tmpFaceArray = np.zeros((3,), dtype = np.int)
                for j in range(0, 3):
                    if tmpFace[j] == '' :
                        tmpFaceArray[j] = 0
                    else:
                        tmpFaceArray[j] = int(tmpFace[j])

                lineFaceArray = np.r_[lineFaceArray, [tmpFaceArray]]

            faceCount[tempCount] += 1
            lineFaceArray = np.delete(lineFaceArray , (0), axis = 0)
            gFaceArrays[gTotalFace].getFaceToArr(lineFaceArray)
            gTotalFace += 1

        else :
            continue

    #file read finished 
    #now print
    print("file name: " + paths[0])
    print("total number of faces: " + str(gTotalFace) )
    print("number of faces with 3 vertices: " + str(faceCount[3]))
    print("number of faces with 4 vertices: " + str(faceCount[4]))

    moreThan4 = 0
    for i in range(5, 100):
        moreThan4 += faceCount[i]

    print("number of faces with 5 or more vertices: " + str(moreThan4))

    gVertexArraySeparate = makeTriangle_createVertexArraySeperate()


    # print(gVertexArray)
    # print(gVertexNormalArray)
    # print(gVertexArraySeparate)


def drop_callback(window, paths):
    # reinitialize the whole data structure to read another file.
    global gTotalFace, faceCount, gVertexArray, gVertexNormalArray
    global gVertexArraySeparate, gFaceArrays

    gVertexArray = np.array([[0.,0.,0.]], 'float32')
    gVertexNormalArray = np.array([[0.,0.,0.]], 'float32')
    gFaceArrays = []
    for i in range(0, 1000000):        # 폴리곤의 최대 vertex수에 따라 해당 범위를 바꾸면 됩니다. 
        gFaceArrays.append(FaceArray(i))

    gVertexArraySeparate = np.array([[0.,0.,0.]], 'float32')

    # faceCount[number of vertices] = number of faces
    faceCount = np.zeros((100,), dtype = np.int)
    gTotalFace = 0

    # read file , parse the lines, and store data in the global data structure.
    read_and_print_file(paths)

def main():
    global gVertexArraySeparate
    global gTotalFace, faceCount, gVertexArray, gVertexNormalArray

    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2016026026', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.swap_interval(1)

    count = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        ang = count % 360
        render(ang)
        count += 1
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
            
