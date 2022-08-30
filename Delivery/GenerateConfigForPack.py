import operator
import os.path
from collections import OrderedDict

#Predefine variables
paintList = comp.GetToolList(True, "Paint")
unsortedPaintList = {}  #Unsorted list of selected nodes
exportData = ''  #Export data set
initDialog = {1: {1: "cameraSelect", "Name": "Select camera", 2:"Dropdown", "Options":{1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I"}, "Default": 0},
2: {1: "annoStart", "Name": "Annotation start number", 2:"Text", "ReadOnly":"false", "Lines":1, "Default":1},
3: {1: "sortOrder", "Name": "Horizontal node odrer", 2: "Checkbox", "Default": 1}}
cameraList = ["A","B","C","D","E","F","G","H","I"]  #List of cameras

scriptParams = comp.AskUser("Script parameters", initDialog)  #Get camera name from user
annoNum = int(scriptParams['annoStart'])    #Annotation init 

comp.Lock()
#Sorting node list by Y position in the node flow
for toolToSort in paintList:
    flowSort = comp.CurrentFrame.FlowView
    unsortedX, unsortedY = flowSort.GetPosTable(paintList[toolToSort]).values()
    if scriptParams['sortOrder'] == 0:
        unsortedPaintList[unsortedY] = paintList[toolToSort]
    else:
        unsortedPaintList[unsortedX] = paintList[toolToSort]
sortedByCoord = sorted(unsortedPaintList.items(), key=operator.itemgetter(0))
sortedPaintDict = OrderedDict(sortedByCoord).values() #Sorted list of nodes. Upper node first.

#Generate sorted Paint nodes dictionary
sortedPaintList = {}
for iterIndex in range(len(sortedPaintDict)):
    sortedPaintList[iterIndex] = sortedPaintDict[iterIndex]

#Walk thru all Paint nodes and get timestamps for all strokes in Multistrokes    
for tool in sortedPaintList:
    dump = sortedPaintList[tool].SaveSettings() #Get all settings from node as dict.
    comment = sortedPaintList[tool].GetInput("Comments")  #Get Comments field value. Used for keeping annotated object name
    unsortedToolFrameList = []
    for toolstruct in dump['Tools']:
        if "Multi" in toolstruct:  #Find all "Multistroke" keys
            for strokelist in dump['Tools'][toolstruct]:
                if "Strok" in strokelist: # Find all Strokes in each Multistroke
                    for stroke in dump['Tools'][toolstruct][strokelist]:
                        unsortedToolFrameList.append(int(dump['Tools'][toolstruct][strokelist][stroke]['Time'])) 
    toolFrameList = list(set(unsortedToolFrameList))    #Remove duplicated frame numbers
    toolFrameList.sort() #Sort frame numbers
    frameListLen = len(toolFrameList)
    refFrame = 0
    
    #Parse all timestamp ranges 
    if frameListLen == 3:  #If we have 3 diferent points - In, Out and Ref 
        refFrame = toolFrameList[1]
        exportData += str(cameraList[int(scriptParams['cameraSelect'])]) + ":" + str(annoNum) + ":" + str(int(toolFrameList[0])) + ":" + str(int(toolFrameList[2])) + "\n"
        annoNum += 1
    elif frameListLen == 2: #If we have 2 diferent points (In and Out), assume that In and Ref coincide
        refFrame = toolFrameList[0]
        exportData += str(cameraList[int(scriptParams['cameraSelect'])]) + ":" + str(annoNum) + ":" + str(int(toolFrameList[0])) + ":" + str(int(toolFrameList[1])) + "\n"
        annoNum += 1
    else:  #If we have more or less than 2 or 3 points - assume whe have mistake in strokes
        exportData += str(cameraList[int(scriptParams['cameraSelect'])]) + ":Broken range.\n"
        annoNum += 1 
comp.Unlock()
fileName = os.path.dirname(comp.GetAttrs("COMPS_FileName")) + "\\packlist_cam-" + str(cameraList[int(scriptParams['cameraSelect'])]) + ".txt"  #Generate path and filename
with open(fileName,'a') as f:
    f.write(exportData)
    print("Job done! Config file ready.")
