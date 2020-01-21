import functools
import pymel.core as pm
import re

meshName = ['']
copied = ['False']

def createUI( pWindowTitle ):
	windowID = 'myWindowID'
	
	if pm.window(windowID, exists = True):
	    pm.deleteUI( windowID )
	   
	pm.window(windowID, title = pWindowTitle, widthHeight = (300, 59))

	pm.columnLayout(adjustableColumn = True)

	pm.separator(height = 4, style = 'none')

	pm.button(label = 'copy vertex positions', command = copyCallbackDecide, backgroundColor = (0.066,0.447,0.443))

	pm.separator(height = 4, style = 'none')
	
	if copied[0] == 'True':
	    pm.button(label = 'paste vertex positions', command = pasteCallback, backgroundColor = (0.109,0.227,0.29))
	if copied[0] == 'False':
	    pm.button(label = 'paste vertex positions', command = pasteCallbackNull, backgroundColor = (0.321,0.321,0.321))

	pm.separator(height = 4, style = 'none')

	pm.setParent('..')

	pm.showWindow()
	
def copyCallbackDecide(*pArgs):
    selection = pm.ls(sl = True)[0]
    if isinstance(selection, pm.MeshVertex):
        copyCallback()
    else:
        print('Select the verticies you want to copied')

def copyCallback(*pArgs):
	#this script takes the selection and outputs it as a list of vertex positions
	selection = pm.ls(sl = True)
	    
	getVecList = []
	tempList = []

	for item in selection:
	    myVals = pm.xform(item,query = True, translation = True, worldSpace = True)
	    for position in myVals:
	        tempList.append(position)
	        
	myX = tempList[::3]
	myY = tempList[1::3]
	myZ = tempList[2::3]
	
	index = 0
	
	while(index < len(tempList)/3):
	    myVec = ['','','']
	    myVec[0] = myX[index]
	    myVec[1] = myY[index]
	    myVec[2] = myZ[index]
	    #getVecList.append(myVec)
	    getVecList.append('%s,%s,%s'%(myX[index],myY[index],myZ[index]))
	    index = index + 1

	vertexPosRead = open('D:/NewCompany/Characters/Scripts/SelectedVertexPositions.txt','w')
	vertexPosRead.write('')
	#vertexPosRead.write(getVecList)
	for item in getVecList:
	    vertexPosRead.write('%s|'%(item))

	vertexPosRead.close()

	#this section stores the name of the selected object, and writes the vertcies to a file

	myMesh = pm.ls(hl = True)
	for item in myMesh:
		meshName[0] = item
	vtxSelection = pm.ls(sl = True)

	vertexRead = open('D:/NewCompany/Characters/Scripts/SelectedVerticies.txt', 'w')
	vertexRead.write('')

	for item in vtxSelection:
	    pm.select(item)
	    mySel = pm.ls(orderedSelection = True, flatten = True, an = True)
	    for vtx in mySel:
	    	tempValue = re.sub('Shape','','%s,'%(vtx))
    		vertexRead.write(tempValue)
	vertexRead.close()
	
	copied[0] = 'True'
	createUI('Transfer Verts')
	
	print('Copied!')

def pasteCallbackNull(*pArgs):
    print('First select the verticies you want to copy')

def pasteCallback(*pArgs):

	newName = pm.ls(sl = True)[0]

	vtxFile = open('D:/NewCompany/Characters/Scripts/SelectedVerticies.txt', 'r+')
	
	vtxList = []
	
	if meshName[0] == newName:
	    print('select a new object to copy verticies to')
	    
	else:
	    for item in vtxFile.read().split(','):
	        newVtxName = re.sub('%s'%(meshName[0]),'%s'%(newName),item)
	        vtxList.append(newVtxName)
	
	    vtxPosFile = open('D:/NewCompany/Characters/Scripts/SelectedVertexPositions.txt', 'r+')
	
	    vtxPosList = []
	    for item in vtxPosFile.read().split('|'):
	        if item != '':
	            vtxPosList.append(item)
	
	    idx = 0
	    for index in vtxPosList:
	        myVec = index.split(',')
	        pm.xform(vtxList[idx], rfl = True, translation = (float(myVec[0]),float(myVec[1]),float(myVec[2])))
	        idx+=1
	        
	    vtxFile.close()
	    vtxPosFile.close()
	    
	    print('Pasted!')
    
createUI('Transfer Verts')