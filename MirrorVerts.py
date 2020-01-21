import pymel.core as pm

#Mirror Verts

leftBool = ['False']
rightBool = ['False']

leftTextFile = ['']
rightTextFile = ['']

def createUI( pWindowTitle ):
	windowID = 'myWindowID'
	
	if pm.window(windowID, exists = True):
	    pm.deleteUI( windowID )
	   
	pm.window(windowID, title = pWindowTitle, widthHeight = (300, 150))

	pm.columnLayout(adjustableColumn = True)
	pm.separator(height = 10, style = 'none')
	pm.text(label = 'Select Main Object', align = 'center')
	pm.separator(height = 10, style = 'none')
	pm.text(label = 'Copy from which side?', align = 'center')
	pm.separator(height = 20, style = 'none')
	
	pm.rowLayout(nc = 4)
	
	pm.separator(w = 100)
	pm.checkBox(label = 'Left', onCommand = LeftOn, offCommand = LeftOff)
	pm.separator(w = 30)
	pm.checkBox(label = 'Right', onCommand = RightOn, offCommand = RightOff)
	
	pm.setParent('..')
	
	pm.separator(height = 20)
	
	pm.button(label = 'Copy Custom', command = CopyDefault)
	pm.separator(height = 20)
	pm.button(label = 'Copy Face', command = CopyFace)
    
	pm.separator(height = 4, style = 'none')
	
	pm.setParent('..')

	pm.showWindow()
	

def LeftOn(*pArgs):
    leftBool[0] = 'True'
def LeftOff(*pArgs):
    leftBool[0] = 'False'
def RightOn(*pArgs):
    rightBool[0] = 'True'
def RightOff(*pArgs):
    rightBool[0] = 'False'
    
def CopyFace(*pArgs):
    leftTextFile[0] = ('D:\NewCompany\Characters\Scripts\selectedVerticesFaceLeft.txt')
    rightTextFile[0] = ('D:\NewCompany\Characters\Scripts\selectedVerticesFaceRight.txt')
    CopyVerts()
    
def CopyDefault(*pArgs):
    leftTextFile[0] = ('D:\NewCompany\Characters\Scripts\selectedVerticesLeft.txt')
    rightTextFile[0] = ('D:\NewCompany\Characters\Scripts\selectedVerticesRight.txt')
    CopyVerts()
    
def CopyVerts(*pArgs):
    leftVerts = []
    vertPosL = []
    rightVerts = []
    vertPosR = []
    selectedName = pm.ls(sl = True, an = True)[0]
    
    #access the list of saved verticies
    leftVertices = open(leftTextFile[0],'r')
    rightVertices = open(rightTextFile[0], 'r')

    for line in leftVertices.read().split(','):
        if(line != ''):
            newName = line.replace('BaseBlendShape','%s'%(selectedName))
            leftVerts.append(newName)
    for line in rightVertices.read().split(','):
        if(line != ''):
            newName = line.replace('BaseBlendShape','%s'%(selectedName))
            rightVerts.append(newName)
                
    leftVertices.close()
    rightVertices.close()
    
    #create a list of all the mirrored verts
    for vert in leftVerts:
        pos = pm.xform(vert, query = True, t = True)
        vertPosL.append(pos)
        
    for vert in rightVerts:
        pos = pm.xform(vert, query = True, t = True)
        vertPosR.append(pos)
    
    if leftBool[0] == 'True':
        idxL = 0
        for vert in leftVerts:
            newPos = vertPosR[idxL]
            pm.xform(vert, t = (newPos[0]*-1, newPos[1], newPos[2]))
            idxL = idxL + 1
    if rightBool[0] == 'True':
        idxR = 0
        for vert in rightVerts:
            newPos = vertPosL[idxR]
            pm.xform(vert, t = (newPos[0]*-1, newPos[1], newPos[2]))
            idxR = idxR + 1
    
createUI('Mirror Verts')