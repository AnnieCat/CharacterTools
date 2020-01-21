import pymel.core as pm
import maya.OpenMaya as OpenMaya

selectedMeshes = ['']

def createUI(pWindowTitle):
    windowID = 'myWindowID'
    
    if pm.window(windowID, exists = True):
        pm.deleteUI(windowID)
        
    pm.window(windowID, title = pWindowTitle, width = 440)
    
    pm.rowColumnLayout()
    
    #First Button
    pm.separator(h=6, style = 'none')
    pm.text(al = 'left', label = 'Base Mesh:')
    pm.separator(h=6, style = 'none')

    if selectedMeshes[0]=='':
        pm.button(label = 'Select Base Mesh', command = selectBase, height = 30, width = 440)
    else:
        pm.button(label = '%s'%(selectedMeshes[0]), command = selectBase, height = 30, width = 440, backgroundColor = (0.192,0.639,0.745))

    #Second Button
    pm.separator(h=6, style = 'none')
    pm.text(al = 'left', label = 'Select verticies to copy on reference mesh')
    pm.separator(h=6, style = 'none')
    if selectedMeshes[0] != '':
        pm.button(label = 'Copy', command = copyVerts, height = 30, width = 440, backgroundColor = (0.823,0.517,0.439))
    else:
        pm.button(label = 'Copy', command = noWorky, height = 30, width = 440)
    pm.showWindow()
    
def noWorky(*pArgs):
    print('First select your base mesh')
     
def selectBase(*pArgs):
    
    sel = pm.ls(sl = True)
    if sel == []:
        print 'Select Base Mesh!'
    else:
        selectedMeshes[0] = sel[0]
        createUI('Snap Verticies')
    
def copyVerts(*pArgs):
    mainObject = pm.ls(sl = True, o = True)
    subObjects = pm.ls(sl = True)
    
    #if verticies are not selected, do not allow progression
    if mainObject == subObjects:
        print('Please select the verticies of the reference mesh you wish to copy')
    if mainObject != subObjects:
        nodeDagPath = OpenMaya.MObject()
        geo = selectedMeshes[0]
        
        #create an empty DAG path and populate it with our Base Mesh
        try:
            selectionList = OpenMaya.MSelectionList()
            selectionList.add(geo.name())
            nodeDagPath = OpenMaya.MDagPath()
            selectionList.getDagPath(0, nodeDagPath)
        except:
            raise RuntimeError('OpenMaya.MDagPath() failed on %s'% geo.name())
        
        #Derive the functional surface from our sphere object
        mfnMesh = OpenMaya.MFnMesh(nodeDagPath)
        
        #Start Loop
        myVerts = pm.ls(sl = True, fl = True)
        for vert in myVerts:
            pos = pm.MeshVertex.getPosition(vert, space = 'world')
            
            #initialize pointA - Reference Mesh Vertex XYZ Data, and PointB - Source Vertex
            pointA = OpenMaya.MPoint(pos.x, pos.y, pos.z)
            pointB = OpenMaya.MPoint()
            space = OpenMaya.MSpace.kWorld
            
            #Create class for working with references and pointers
            util = OpenMaya.MScriptUtil()
            util.createFromInt(0)
            idPointer = util.asIntPtr()
            
            mfnMesh.getClosestPoint(pointA, pointB, space, idPointer)
            idx = OpenMaya.MScriptUtil(idPointer).asInt()
            
            #load all base mesh verticies, referenced by earlier pointer
            faceVerts = [geo.vtx[i] for i in geo.f[idx].getVertices()]
            closestVert = None
            minLength = None
            
            #this might be the part I have to re-think            
            for v in faceVerts:
                thisLength = (pos - v.getPosition(space = 'world')).length()
                if minLength is None or thisLength < minLength:
                    minLength = thisLength
                    closestVert = v
            pm.xform(closestVert, translation = (float(pos.x), float(pos.y), float(pos.z)))
            
    
createUI('Snap Verticies')