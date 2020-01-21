#polyMorph.py

import maya.cmds as cmds
import functools
import pymel.core as pm
import re

globalNameKey = []
globalVertexKey = []
globalGender = ['']

lockedGroups = ['Eye', 'Face', 'Mouth', 'Nose']
rolloutGroups = ['modellingToolkit','EyeShapes','bodypartSelection','bakeModel']
rolloutBools  = [True,True,True,True]

globalEyeKey = []
globalEyeIndex = 0
globalMouthKey = []
globalMouthIndex = 0
globalNoseKey = []
globalNoseIndex = 0
jawIsAway = 0
OnStart = 1


def createUI( pWindowTitle ):
    windowID = 'myWindowID'

    globalGender[0] = getGender()

    if cmds.window(windowID, exists = True):
        cmds.deleteUI( windowID )

    cmds.window(windowID, title=pWindowTitle, width = 440)

    # root column layout
    cmds.rowColumnLayout()

    cmds.image(image = 'icons\EqualReality\PolyMorphTitle.jpg')
    
    cmds.button(label='Load Base Model', command=importCallback, height = 50, backgroundColor = (0.066,0.447,0.443))

    cmds.separator(h = 4, style='none', backgroundColor = (0.07,0.121,0.152))

    cmds.button(label = 'Load Photogrammetry Reference', command = importReferenceCallback, height = 35, backgroundColor = (0.109,0.227,0.29))

    #cmds.separator(h = 20, style='none', backgroundColor = (0.133,0.164,0.239))

    #cmds.button(label='Edit', command=editCallback, backgroundColor = (0.109,0.458,0.16))
    cmds.separator(h = 4, style='none', backgroundColor = (0.07,0.121,0.152))
    
    if pm.ls('Trace'):

        #populate my fields by reading the files
        nameKey = []
        nameRead = open('EqualRealityData\SelectionData%s.txt'%(globalGender[0]), 'r+')
        vertexRead = open('EqualRealityData\SelectedVerticies%s.txt'%(globalGender[0]), 'r+')
        eyeRead = open('EqualRealityData\SavedVertexPositions%sEye.txt'%(globalGender[0]), 'r+')
        for line in nameRead.readlines():
            mySelName = re.sub('\r\n','',line)
            nameKey.append(mySelName)
            if globalNameKey.count(mySelName) < 1:
                globalNameKey.append(mySelName)
        for line in vertexRead.read().split('\r\n\r\n'):
            if line not in globalVertexKey:
                globalVertexKey.append(line)

        for line in eyeRead.read().split('\r\n\r\n'):
            if line != None and line not in globalEyeKey:
                globalEyeKey.append(line)

        eyeRead.close()
        nameRead.close()
        vertexRead.close()

        pm.softSelect(softSelectEnabled = True)
        pm.symmetricModelling(s=True)

        cmds.separator(h = 8, style='none', backgroundColor = (0.07,0.121,0.152))
        pm.rowColumnLayout(numberOfColumns = 2, columnWidth = [(1,120),(2,325)])
        pm.separator(style = 'none', backgroundColor = (0.27, 0.345, 0.376))
        pm.checkBox('GuidesVisible', label = 'Show Guides for Reference Alignment', height = 25, 
                    backgroundColor = (0.27, 0.345, 0.376),
                    onCommand = referenceLines, offCommand = referenceLines)
        pm.setParent('..')
        cmds.separator(h = 4, style='none', backgroundColor = (0.07,0.121,0.152))

        global OnStart
        if OnStart == 1:
            print('this is the first time ive run')
            moveJaw('Away')
            OnStart = 0

        myState = rolloutParameters(name = 'modellingToolkit', query = True)
        cmds.frameLayout(backgroundColor = (0.301, 0.423, 0.513), collapsable = True, collapse = myState, label = 'Modelling Toolkit')

        cmds.separator(h = 2, style='none')

        #Pick Eye Shape
        createImageButtonGroup('Eye')
        cmds.setParent('..')

        myState = rolloutParameters(name = 'bodypartSelection', query = True)
        cmds.frameLayout(backgroundColor = (0.25, 0.349, 0.423), collapsable = True, collapse = myState, label = 'Bodypart Selection')
        cmds.rowColumnLayout(numberOfColumns = 3, columnWidth = [(1,380),(2,30),(3,30)])

        cmds.rowColumnLayout(numberOfColumns = 3, columnWidth = [(1, 80), (2,180), (3,115)])
        cmds.text(label = '   Soft Select:  ', align = 'left')
        cmds.floatSlider("SoftSelectSlider", changeCommand = sliderChangeCommand, min= 0, max = 8)
        cmds.text(label = '     Move Jaw Away     ', align = 'right')


        cmds.setParent('..')
        #cmds.setParent('..')

        cmds.checkBox(value = jawIsAway, label = '', onCommand = functools.partial(moveJaw, 'Away'), offCommand = functools.partial(moveJaw, 'Back'))
        
        cmds.separator(h=20, style ='none')

        cmds.separator(h=20, style ='none')
        cmds.separator(h=20, style ='none')
        cmds.separator(h=20, style ='none')

        global lockedGroups

        for pSelection in nameKey:
            bodypartSelection(pSelection)
            cmds.separator(h=20, style = 'none')
            #lock perminant entries
            if pSelection in lockedGroups:
                cmds.separator(h=20, style = 'none')
            else:
                cmds.button('DeleteButton%s'%(pSelection), label = 'X', backgroundColor = (0.815, 0.098, 0.098), command = functools.partial(removeButtonCallback , pSelection))

        cmds.setParent('..')

        pm.separator(h = 5, style = 'none')
        pm.textFieldButtonGrp("addingNewFields", label = 'New Type:   ', placeholderText = '  selection name...', buttonLabel = 'Add', buttonCommand = addButtonCallback)
        
        cmds.separator(h = 5, style = 'none')
        
        cmds.setParent('..')
        cmds.setParent('..')

        myState = rolloutParameters( name = 'bakeModel', query = True )
        cmds.frameLayout(backgroundColor = (0.329, 0.482, 0.431), collapsable = True, collapse = myState, label = 'Bake Model')
        cmds.separator(h = 4, style = 'none')
        cmds.button(backgroundColor = (0.235, 0.388, 0.349), label = 'Place Eyes', command = eyesCallback )
        #cmds.separator(h = 4, style = 'none')        
        cmds.button(backgroundColor = (0.235, 0.388, 0.349), label = 'Bake', command = bakeCallback )        
        cmds.setParent('..')
    cmds.showWindow()

def rolloutParameters( names = [], name = '', edit = False, query = False ):
    global rolloutGroups
    global rolloutBools

    if edit == True:
        index = 0
        for item in rolloutGroups:
            if item in names:
                rolloutBools[index] = False
            else:
                rolloutBools[index] = True
            index = index + 1
    if query == True:
        myIndex = rolloutGroups.index(name)
        return rolloutBools[myIndex]

def createImageButtonGroup( groupName = '' ):
    myState = rolloutParameters(name = '%sShapes'%(groupName), query = True)
    cmds.frameLayout(backgroundColor = (0.25, 0.349, 0.423),collapsable = True, collapse = myState, label = '%s Shapes'%(groupName))
    cmds.rowColumnLayout(numberOfColumns = 5, columnWidth = [(1,88),(2,88),(3,88),(4,88),(5,88)])
    
    cmds.separator(h = 15, style = 'none')
    cmds.separator(h = 15, style = 'none')
    cmds.separator(h = 15, style = 'none')
    cmds.button("add%sShape" % (groupName), label = 'Add', command = functools.partial(addIconButton, groupName), backgroundColor = (0.145,0.541,0.18))
    cmds.button("remove%sShape"%(groupName), label = 'Remove', command = functools.partial(removeIconButton, groupName), backgroundColor = (0.815,0.098,0.098))
    
    createImageButtons(groupName = groupName)

    cmds.setParent('..')

def createImageButtons( groupName = '' ):
    myNames = getImageNames(groupName = groupName)
    index = 0
    neutralColor = (0.266,0.266,0.266)
    selectedColor = (0.93,0.854,0.0) 
    print('xxx startingIndex = %s, globalEyeIndex = %s'%(index, globalEyeIndex))
    for item in myNames:
        if index == globalEyeIndex:
            print('createImageButtons active index: %s'%(index))
            pm.iconTextButton("%s" % (myNames[index]), imageOverlayLabel  = myNames[index], command = functools.partial(loadIconButton, groupName, index), backgroundColor = selectedColor, image = 'icons/EqualReality/%s_%s.iff'%(myNames[index],globalGender[0]), width = 88, height = 88)
        else:
            print('createImageButtons inactive index: %s'%(index))
            pm.iconTextButton("%s" % (myNames[index]), imageOverlayLabel = myNames[index], command = functools.partial(loadIconButton, groupName, index), backgroundColor = neutralColor, image = 'icons/EqualReality/%s_%s.iff'%(myNames[index],globalGender[0]), width = 88, height = 88)
        index = index + 1

def getImageNames(groupName = ''):
    buttonNames = open('EqualRealityData\%sShapes%s.txt'%(groupName, globalGender[0]), 'r')
    myNames = buttonNames.read().split('\r\n')
    buttonNames.close()

    return myNames

def bodypartSelection( pSelectionName ):
    cmds.button("button_%s"%(pSelectionName), label = pSelectionName, command= functools.partial(selectionCallback, pSelectionName))

def sliderChangeCommand(*Args ):
    pValue = pm.floatSlider("SoftSelectSlider", query = True, value = True)
    pm.softSelect(softSelectDistance = pValue)

    print(pValue)

def referenceLines( *pArgs):
    boolChk = pm.checkBox('GuidesVisible', value = True, query = True)
    if boolChk == True:
        pm.showHidden('Trace')
    if boolChk == False:
        pm.hide('Trace')

def addButtonCallback( *Args ):
    pValue = pm.textFieldButtonGrp("addingNewFields", query = True, text = True)
    cmds.selectPref(trackSelectionOrder = True)
    mySelection = cmds.ls( os = True )
    
    nameWrite = open('EqualRealityData\SelectionData%s.txt'%(globalGender[0]), 'a')
    vertexWrite = open('EqualRealityData\SelectedVerticies%s.txt'%(globalGender[0]), 'a')

    if(pValue not in globalNameKey):
        if cmds.ls(sl=True)==[]:
            print('nothing is selected')
        else:
            nameWrite.write('\r\n%s' % (pValue))
            vertexWrite.write('\r\n\r\n')
            for item in mySelection:
                vertexWrite.write('%s,'%(item))
            vertexWrite.close()
            nameWrite.close()
            pm.select(clear = True)

            rolloutParameters(names = ['modellingToolkit','bodypartSelection'], edit = True)
            createUI('Poly Morph')
    else:
        fileWrite.close()
        print('Cant add... thats a duplicate!')

def removeButtonCallback( pSelection, *Args ):
    if pSelection in globalNameKey:
        myPosition = globalNameKey.index(pSelection)
        globalVertexKey.pop(myPosition)
        globalNameKey.remove(pSelection)
        lastItem = globalNameKey[-1]
        lastVertex = globalVertexKey[-1]
        writeToList(lastItem, lastVertex)
    else:
        print('%s is not on my list'%(pSelection))

def loadIconButton( pGroupName, pButtonIndex, *Args):
    global globalEyeIndex
    global globalEyeKey

    globalEyeIndex = pButtonIndex
    print('XXX loadIconButton pButtonIndex: %s'%(pButtonIndex))
    print('XXX loadIconButton global eye index: %s'%(globalEyeIndex))
    setVertexPositions(pGroupName)
    rolloutParameters(names = ['modellingToolkit','EyeShapes'], edit = True)
    createUI('Poly Morph')
#xxx
def removeIconButton( gName, *Args):
    global globalEyeIndex
    global globalEyeKey  #global eye key is the saved vertex positions

    localNameKey = []

    if globalEyeIndex == 0:
        print('Cant delete the default state')
    else:
        savedNamesRead = open('EqualRealityData\EyeShapes%s.txt'%(globalGender[0]), 'r+')
        for item in savedNamesRead:
            localNameKey.append(item)

        pm.sysFile('icons\EqualReality\%s_%s.iff'%(localNameKey[globalEyeIndex],globalGender[0]), delete = True)
        del localNameKey[globalEyeIndex]
        #created a local list of the eye names sans deleted one, and deleted the associated image

        lastNameOnList = len(localNameKey)
        tempVal = re.sub('\r\n','', localNameKey[lastNameOnList-1])
        localNameKey[lastNameOnList - 1] = tempVal
        savedNamesRead.close()
        #removed spaces from last line of global name key

        del globalEyeKey[globalEyeIndex]
        globalEyeIndex = globalEyeIndex - 1
        savedNames = open('EqualRealityData\%sShapes%s.txt'%(gName, globalGender[0]), 'w+')
        savedPositions = open('EqualRealityData\SavedVertexPositions%s%s.txt'%(globalGender[0], gName), 'w+')
        lastItemInVtxKey = len(globalEyeKey)-1
        index = 0
        for item in globalEyeKey:
            if index != lastItemInVtxKey:
                savedPositions.write('%s\r\n\r\n'%(item))
            else:
                savedPositions.write('%s'%(item))
            index = index + 1
        for item in localNameKey:
            savedNames.write('%s'%(item))

        savedNames.close()
        savedPositions.close()

        setVertexPositions(gName)

        rolloutParameters(names = ['modellingToolkit','EyeShapes'], edit = True)
        createUI('Poly Morph')

def addIconButton(gName,*Args):
    global globalEyeIndex
    currentSelection = getVertexPositions()
    currentSelectionStrings = []
    for index in currentSelection:
        currentSelectionStrings.append('%s'%(index))
    
    #read saved data
    storedList = open('EqualRealityData\SavedVertexPositions%s%s.txt'%(globalGender[0],gName), 'r+')
    # to read
    savedVecList = []
    arrayOfSaves = storedList.read().split('\r\n\r\n')
    arrayOfSaves = filter(None, arrayOfSaves)
    for index in arrayOfSaves:
        savedList = index.split('|')
        savedList = filter(None, savedList)
        savedVecList.append(savedList)


    #check for new button.  If not exists, make one
    activeIndex = -1
    tempIndex = -1
    for item in savedVecList:
        if item == currentSelectionStrings:
            activeIndex = savedVecList.index(item)
        else:
            tempIndex = savedVecList.index(item)
    
    
    #if there is no match
    if(activeIndex==-1):
        globalEyeIndex = tempIndex +1
        namePopup()
    else:
        print('This pose already exists')
    storedList.close()

    #globalEyeIndex = globalEyeIndex + 1
    #if(activeIndex>0):
    #    globalEyeIndex = activeIndex
    #else:
    #    globalEyeIndex = 0

def editCallback( *pArgs ):
    print("not connected to anything")

def shaderSwitch( pRenderStyle, *Args):

    skinMat = getMaterial('Eyelashes')
    fillMat = getMaterial('blocker')

    if pRenderStyle == 'Normal':
        applyMatToSelection(skinMat, ['Body_%s'%(globalGender[0]),'Eyes'])
        pm.hide('Eyes','blocker','IconRenderer')
        pm.showHidden('Eyelashes')

    if pRenderStyle == 'Flat':
        applyMatToSelection(fillMat, ['Body_%s'%(globalGender[0]),'Eyes'])
        pm.showHidden('Eyes','blocker','IconRenderer')
        pm.hide('Eyelashes')


def getMaterial( pObject, *Args ):
    skinObject = pm.ls(pObject, dagObjects = True, objectsOnly=True,shapes=True)
    shadingGroups = pm.listConnections(skinObject, type = 'shadingEngine')
    selectionMaterial = pm.ls(pm.listConnections(shadingGroups), materials = True)
    
    return selectionMaterial[0]
    

def applyMatToSelection(pMaterial, pSelection):
    shader = pm.sets( renderable = True, noSurfaceShader = True, empty = True, name = "thisSurfaceShader")
    pMaterial.outColor >> shader.surfaceShader

    mySel = pm.ls(sl=True)
    pm.sets(shader, edit = True, forceElement = pSelection)


def changeColors(*Args):
    myFill = pm.shadingNode("aiFlat", asShader = True, name = 'Fill') 
    myFill.setAttr("color", (0.066,0.066,0.066))
    
    myWire = pm.shadingNode("aiWireframe", asShader = True, name = 'Wireframe') 
    myWire.setAttr("lineColor", (0.066,0.505,0.215))
    myWire.setAttr("fillColor", (0.07,0.066,0.066))
    myWire.setAttr("edgeType", 'polygons')

    wireShader = pm.sets( renderable = True, noSurfaceShader = True, empty = True, name = "wireSurfaceShader")
    myWire.outColor >> wireShader.surfaceShader

    pm.sets(wireShader, edit = True, forceElement=['Body_%s'%(globalGender[0])])

def namePopup( *Args):
    windowID = 'popupID'
    if cmds.window(windowID, exists = True):
        cmds.deleteUI( windowID )
    
    cmds.window(windowID, title='New Entry',backgroundColor = (0.3,0.3,0.3), titleBar = True, toolbox = True, width = 100)
    cmds.rowColumnLayout()
    cmds.separator(height = 5, style = 'none')
    cmds.text('Describe %s shape: '%(globalNameKey[0]))
    cmds.separator(height = 5, style = 'none')
    cmds.textField("Name_Textfield",width = 100)
    cmds.separator(height = 10, style = 'none')
    cmds.rowColumnLayout(numberOfColumns = 4)
    cmds.separator(height = 20, w = 30, style = 'none')
    cmds.button(label = ' Save ',command = saveName, backgroundColor = (0.43,0.43,0.43))
    cmds.separator(height = 20, w = 15, style = 'none')
    cmds.button(label = 'Cancel', command = functools.partial(cancelName, 'popupID'), backgroundColor = (0.43,0.43,0.43))
    cmds.showWindow()

def saveName( *pArgs):
    #save the vertex positions
    currentSelection = getVertexPositions()
    storedList = open('EqualRealityData\SavedVertexPositions%s.txt'%(globalGender[0]), 'a')
    
    storedList.write('\r\n\r\n')
    for item in currentSelection:
        storedList.write('%s|'%(item))

    storedList.close()

    #save the name
    myText = cmds.textField("Name_Textfield", query = True, text = True)
    myNames = open('EqualRealityData\EyeShapes%s.txt'%(globalGender[0]),'a')
    myNames.write('\r\n%s'%(myText))
    myNames.close()

    shaderSwitch('Flat')

    myWindow = pm.window('Icon Render')
    form = pm.formLayout()
    editor = pm.modelEditor()
    column = pm.columnLayout('true')
    pm.formLayout( form, edit=True, attachForm=[(column, 'top', 0), (column, 'left', 0), (editor, 'top', 0), (editor, 'bottom', 0), (editor, 'right', 0)], attachNone=[(column, 'bottom'), (column, 'right')], attachControl=(editor, 'left', 0, column))
    myCam = 'IconRendererShape'
    pm.modelEditor(editor, activeView = True, camera=myCam, displayTextures = True, edit=True, displayAppearance='smoothShaded')
    pm.showWindow( myWindow )
    
    pm.select('Body_%s'%(globalGender[0]))
    pm.playblast(completeFilename = "%s_%s.iff"%(myText,globalGender[0]), viewer = False, showOrnaments = False, frame = [1], percent = 100, format = "image", width = 84, height = 84)
    
    shaderSwitch ( 'Normal' )

    pm.deleteUI( myWindow )
    cmds.deleteUI( 'popupID' )

    globalEyeKey = []

    rolloutParameters(names = ['modellingToolkit','EyeShapes'], edit = True)
    createUI('Poly Morph')

def cancelName( windowToDelete, *Args ):
    cmds.deleteUI(windowToDelete)

def setVertexPositions( pBodyPart, *Args ):
    global globalEyeIndex
    listOfNames = open('EqualRealityData\SelectionData%s.txt'%(globalGender[0]), 'r')
    localListOfNames = listOfNames.read().split('\r\n')
    index = 0
    myVtxIndex = 0
    origRead = []
    for item in localListOfNames:
        if item == pBodyPart:
            origRead = globalVertexKey[index].split(',')
            myVtxIndex = index
        index = index + 1
    listOfNames.close()
    origRead = filter(None, origRead)
    pVertexList = origRead
    myVtxList = open('EqualRealityData\SavedVertexPositions%s%s.txt'%(globalGender[0],pBodyPart), 'r')

    posList = myVtxList.read().split('\r\n\r\n')
    myNewPos = posList[globalEyeIndex].split('|')
    myVtxList.close()
    vtxIndex = 0
    for item in pVertexList:
        pm.select(item)
        mySel = pm.ls(orderedSelection = True, flatten = True, an = True)
        for vtx in mySel:
            #print('vtx name %s, pos %s'%(vtx,myNewPos[vtxIndex]))
            currentPos = myNewPos[vtxIndex][1:-1].split(',')
            pm.xform(vtx, translation = (float(currentPos[0]),float(currentPos[1]),float(currentPos[2])))
            vtxIndex = vtxIndex + 1
        pm.select(clear = True)

#here
def getVertexPositions( *pArgs ):
    origRead = globalVertexKey[0].split(',')
    origRead = filter(None, origRead)
    pVertexList = origRead
    getVecList = []
    tempList = []

    for item in pVertexList:
        myVals = cmds.xform(item,query = True, translation = True, worldSpace = True)
        for position in myVals:
            tempList.append(position)

    myX = tempList[::3]
    myY = tempList[1::3]
    myZ = tempList[2::3]

    index = 0
    while(index < len(tempList)/3):
        myVec = [myX[index],myY[index],myZ[index]]
        getVecList.append(myVec)
        index = index + 1
    return getVecList



def writeToList( pLastItem, pLastVertex ):
    (globalGender[0]) = getGender()
    nameWrite = open('EqualRealityData\SelectionData%s.txt'%(globalGender[0]), 'w')
    vertexWrite = open('EqualRealityData\SelectedVerticies%s.txt'%(globalGender[0]), 'w')

    for item in globalNameKey:
        if(item == pLastItem):
            nameWrite.write(item)
        else:
            nameWrite.write('%s\r\n'%(item))

    for item in globalVertexKey:
        if(item == pLastVertex):
            vertexWrite.write(item)
        else:
            vertexWrite.write('%s\r\n\r\n'%(item))
    nameWrite.close()
    vertexWrite.close()

    rolloutParameters(names = ['modellingToolkit','bodypartSelection'], edit = True)
    createUI('Poly Morph')

def getGender():
    myObjects = pm.ls(geometry = True, visible = True)
    myGender = ''

    if 'Body_FemaleShape' in myObjects:
        myGender = 'Female'
    if 'Body_MaleShape' in myObjects:
        myGender = 'Male'

    return myGender

def moveJaw(pAwayOrBack, *Args ):
    pm.softSelect(softSelectEnabled = False)
    global jawIsAway
    if globalGender[0] == 'Female':
        jawSelection = pm.select('Body_Female.vtx[8267:9986]')
    if globalGender[0] == 'Male':
        jawSelection = pm.select('Body_Male.vtx[12853:14572]')
    pm.symmetricModelling(s=False)
    if(pAwayOrBack == 'Away'):
        pm.xform(translation=(0,0,-200), relative = True)
        jawIsAway = 1
    if(pAwayOrBack == 'Back'):
        pm.xform(translation=(0,0,200), relative = True)
        jawIsAway = 0
    pm.softSelect(softSelectEnabled = True)
    pm.symmetricModelling(s=True)

def selectionCallback(pSelectionName, *Args):
    #Connect slider to soft select
    myPosition = globalNameKey.index(pSelectionName)
    mySelection = globalVertexKey[myPosition]
    myVerticies = mySelection.split(',')
    pm.select(clear = True)
    for item in myVerticies:
        pm.select(item, add = True)

def saveReferenceName( pReferenceObject, *pArgs):
    newLayer = pm.createDisplayLayer(name = 'Scan')
    if(newLayer == 'Scan1'):
        pm.delete('Scan1')
    pm.editDisplayLayerMembers('Scan', pReferenceObject)
    myDescription = pm.textField("referenceDescription", query = True, text = True)
    pm.rename('%s'%(pReferenceObject), 'Scan_%s'%(myDescription))
    pm.deleteUI('referenceID')
    
def importReferenceCallback( *pArgs ):
    mySelection = pm.fileDialog2(caption = 'Import', fileFilter = '*.fbx', fileMode = 4, dialogStyle = 2, okCaption = 'Select Directory')
    newObjects = importWithComparison(mySelection[0])

    windowID = 'referenceID'
    globalGender[0] = getGender()

    if cmds.window(windowID, exists = True):
        cmds.deleteUI( windowID )

    pm.window(windowID, resizeToFitChildren  = True, title = 'Import Reference')
    pm.rowColumnLayout(numberOfColumns = 1)
    pm.text(label = 'Describe your reference:')
    pm.textField("referenceDescription", width = 200)
    pm.rowColumnLayout(numberOfColumns = 3)
    pm.separator(width = 100, style = 'none')
    pm.button(label = 'Save', width = 50, command = functools.partial(saveReferenceName, newObjects))
    pm.button(label = 'Cancel', width = 50, command = functools.partial(cancelName, windowID))
    pm.setParent('..')
    pm.setParent('..')

    pm.showWindow(windowID)

def importWithComparison( pFilename, *pArgs):
    objectsInScene = pm.ls(objectsOnly = True)
    pm.mel.FBXImport(f= pFilename )
    newObjectsInScene = pm.ls(objectsOnly = True)

    for item in newObjectsInScene:
        if item not in objectsInScene:
            return item


def importCallback( *Args ):
    loadPopup = pm.confirmDialog(title = 'Import', message = 'Choose Gender: ', button = ['Female','Male','Cancel'], dismissString = 'Cancel')
    global globalGender
    localGender = ''
    if loadPopup == 'Cancel':
        return
    else:
        cmds.NewScene()
        globalNameKey[:] = []
        globalVertexKey[:] = []
    if loadPopup=='Female':
        pm.mel.FBXImport(f="assets\EqualReality\NudeFemale.fbx")
        localGender = 'Female'
        pm.move('persp',[0,156,89])
    if loadPopup == 'Male':
        pm.mel.FBXImport(f="assets\EqualReality\NudeMale.fbx")
        localGender = 'Male'
        pm.move('persp',[0,169,89])
    pm.rotate('persp',[-8,0,0])

    myScene = ['Eyes','Eyelashes','Body_%s'%(localGender)]
    pm.createDisplayLayer(name = 'Game_Model', number = 1)
    for item in myScene:
       pm.editDisplayLayerMembers('Game_Model', item)
    #pm.hide('mixamorig:Hips')
    pm.hide('Eyes')

    global OnStart
    OnStart = 1

    pm.modelEditor('modelPanel4', edit = True, displayTextures = True)
    rolloutParameters(names = [None], edit = True)
    createUI('Poly Morph')

def eyesCallback( *Args ):
    pm.showHidden('Eyes')
    pm.select('mixamorig:RightEye','mixamorig:LeftEye')

def bakeCallback( *pArgs ):
    print('cake is in the oven')


createUI('Poly Morph')