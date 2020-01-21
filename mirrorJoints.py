import pymel.core as pm

#meshName = ['']
#copied = ['False']

def createUI( pWindowTitle ):
	windowID = 'myWindowID'
	
	if pm.window(windowID, exists = True):
	    pm.deleteUI( windowID )
	   
	pm.window(windowID, title = pWindowTitle, widthHeight = (300, 30))

	pm.columnLayout(adjustableColumn = True)

	pm.separator(height = 25, style = 'none')

	pm.button(label = 'copy bones to other side', command = copyBonesCallback)

	pm.separator(height = 4, style = 'none')
	
	pm.setParent('..')

	pm.showWindow()
	
def copyBonesCallback(*pArgs):
    boneList = pm.ls(sl = True)

    myPrefix = ''
    if (boneList[0][:1]=='L'):
        myPrefix = 'L'
    if (boneList[0][:1]=='R'):
        myPrefix = 'R'
        
    for bone in boneList:
        pm.select(bone)
        newTrans = pm.xform(query = True, translation = True, a = True)
        newRot = pm.xform(query = True, rotation = True)
        if myPrefix == 'L':
            pm.select('R'+bone[1:])
        if myPrefix == 'R':
            pm.select('L'+bone[1:])
        pm.xform(t = (newTrans[0],newTrans[1],-1*(newTrans[2])))
        pm.xform(ro = (newRot[0],newRot[1],-1*(newRot[2])))

	
    
createUI('Transfer Verts')