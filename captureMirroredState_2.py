import pymel.core as pm
import functools
import math

#Capture Vertex Positions

progressTotal = ['10']
percentageStep = ['0']

def createUI( pWindowTitle ):
	windowID = 'myWindowID'
	
	if pm.window(windowID, exists = True):
	    pm.deleteUI( windowID )
	   
	pm.window(windowID, title = pWindowTitle, widthHeight = (300, 30))

	pm.columnLayout(adjustableColumn = True)

	pm.separator(height = 8, style = 'none')
	pm.text(label = 'Select Verticies to copy', align = 'center')
	pm.separator(height =10, style = 'none')
	pm.button(label = 'Capture Vertecies', command = CaptureVtx)
	pm.separator(height = 10, style = 'none')
	pm.setParent('..')

	pm.setParent('..')

	pm.showWindow()
	
def CaptureVtx( sSelection, *pArgs): 
    selVerts = pm.ls(sl = True, fl = True)
    polycount = len(selVerts)
    selectedObj = pm.ls(sl = True, o = True)[0]
    progressTotal[0] = len(selVerts)
    
    #clear the file
    selectedVerticesLeft = open('D:\NewCompany\Characters\Scripts\selectedVerticesLeft.txt','w')
    selectedVerticesRight = open('D:\NewCompany\Characters\Scripts\selectedVerticesRight.txt','w')
    selectedVerticesLeft.write('')
    selectedVerticesRight.write('')
    selectedVerticesLeft.close()
    selectedVerticesRight.close()
    
    selectedVerticesLeft = open('D:\NewCompany\Characters\Scripts\selectedVerticesLeft.txt','a')
    selectedVerticesRight = open('D:\NewCompany\Characters\Scripts\selectedVerticesRight.txt','a')
    
    #for each vertex is the list of selected vertices
    greaterIdxPercent = 0
    lastPercentageTotal = 0
    percentOfTotal = 0
    
    leftVerts = []
    rightVerts = []
    
    for vert in selVerts:
        vertPos = pm.xform(vert, query = True, translation = True, ws = True)
        #Organize Verts into Left, Right and Center

        if int(vertPos[0]*1000) < 0:
            leftVerts.append(vert)
        else:
            rightVerts.append(vert)
    
    idxPercent = 0
    for lVert in leftVerts:
        leftVertPos = pm.xform(lVert, query = True, translation = True, ws = True)
        mirroredVertFlat = [math.floor((leftVertPos[0]*-1)*1000),math.floor(leftVertPos[1]*1000),math.floor(leftVertPos[2]*1000)]
        
        
        
        for rVert in rightVerts:
            rightVertPos = pm.xform(rVert, query = True, translation = True, ws = True)
            rightVertFlat = [math.floor(rightVertPos[0]*1000),math.floor(rightVertPos[1]*1000),math.floor(rightVertPos[2]*1000)]
            
            if mirroredVertFlat[0] < rightVertFlat[0] + 2 and mirroredVertFlat[0] > rightVertFlat[0] - 2:
                if mirroredVertFlat[1] < rightVertFlat[1] + 2 and mirroredVertFlat[1] > rightVertFlat[1] - 2:
                    if mirroredVertFlat[2] < rightVertFlat[2] + 2 and mirroredVertFlat[2] > rightVertFlat[2] - 2:
                        selectedVerticesLeft.write('%s,'%(lVert))
                        selectedVerticesRight.write('%s,'%(rVert))
                        idxPercent = idxPercent + 1
                        print('%s Percent Complete'%((float(idxPercent) / float(len(leftVerts))*100)))
                        break
    selectedVerticesLeft.close()
    selectedVerticesRight.close()
    pm.deleteUI('myWindowID')
    
createUI('Capture Vertices')