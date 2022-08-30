import operator
import os.path
from collections import OrderedDict

#Predefine variables
paintList = comp.GetToolList(True, "Paint")
unsortedPaintList = {}  #Unsorted list of selected nodes
exportData = ''  #Export data set
initDialog = {1: {1: "cameraSelect", "Name": "Select camera", 2:"Dropdown", "Options":{1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I"}, "Default": 0},
2: {1: "cameraSelectConnected", "Name": "Select connected camera", 2:"Dropdown", "Options":{1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I"}, "Default": 0},
3: {1: "annoStart", "Name": "Annotation start number", 2:"Text", "ReadOnly":"false", "Lines":1, "Default":1},
4: {1: "writeFile", "Name": "Write text for spreadsheet", 2: "Checkbox", "Default": 1},
5: {1: "sortOrder", "Name": "Horizontal node odrer", 2: "Checkbox", "Default": 1},
6: {1: "takeScreenshot", "Name": "Generate screenshots", 2: "Checkbox", "Default": 1}}
cameraList = ["A","B","C","D","E","F","G","H","I"]  #List of cameras

scriptParams = comp.AskUser("Script parameters", initDialog)  #Get camera name from user
annoNum = int(scriptParams['annoStart'])    #Annotation init 

comp.StartUndo("Generate annotations") #Start undo loop
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
sortedPaintList = {}
#range(len(sortedPaintDict))
for iterIndex in range(len(sortedPaintDict)):
    sortedPaintList[iterIndex] = sortedPaintDict[iterIndex]
    
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
    if frameListLen == 3:
        refFrame = toolFrameList[1]
        message = "Camera " + str(cameraList[int(scriptParams['cameraSelect'])]) + "\n" + "Annotation " + str(annoNum) + "\n" + "Frame " + str(int(toolFrameList[0])) + " to " + str(int(toolFrameList[2])) + "\n" + "Reference: " + str(int(toolFrameList[1]))
        exportData += str(cameraList[int(scriptParams['cameraSelect'])]) + "\t" + str(annoNum) + "\t" + str(cameraList[int(scriptParams['cameraSelectConnected'])]) + "\t" + comment + "\t" + str(int(toolFrameList[1])) + "\t" + str(int(toolFrameList[0])) + "\t" + str(int(toolFrameList[2])) + "\n"
        annoNum += 1
    elif frameListLen == 2:
        refFrame = toolFrameList[0]
        message = "Camera " + str(cameraList[int(scriptParams['cameraSelect'])]) + "\n" + "Annotation " + str(annoNum) + "\n" + "Frame " + str(int(toolFrameList[0])) + " to " + str(int(toolFrameList[1])) + "\n" + "Reference: " + str(int(toolFrameList[0]))
        exportData += str(cameraList[int(scriptParams['cameraSelect'])]) + "\t" + str(annoNum) + "\t" + str(cameraList[int(scriptParams['cameraSelectConnected'])]) + "\t" + comment + "\t" + str(int(toolFrameList[0])) + "\t" + str(int(toolFrameList[0])) + "\t" + str(int(toolFrameList[1])) + "\n"
        annoNum += 1
    else:
        message = "Annotation " + str(annoNum) + " broken range."
        exportData += str(cameraList[int(scriptParams['cameraSelect'])]) + "\t" + str(annoNum) + "\t" + str(cameraList[int(scriptParams['cameraSelectConnected'])]) + "\tBroken range.\t\n"
        annoNum += 1 
    flow = comp.CurrentFrame.FlowView
    currentNodePosX, currentNodePosY = flow.GetPosTable(sortedPaintList[tool]).values()  #Get current node coordinates
    mergeNode = comp.Merge()  #Create new merge node
    if scriptParams['sortOrder'] == 0:
        flow.SetPos(mergeNode, currentNodePosX + 1, currentNodePosY)  #Move new merge to new position
    else:
        flow.SetPos(mergeNode, currentNodePosX, currentNodePosY - 2)  #Move new merge to new position
    annoTextNode = comp.TextPlus()   #Create new TextPlus node for annotation
    annoTextNode.SetInput("StyledText", message)  #Put text
    if scriptParams['sortOrder'] == 0:
        flow.SetPos(annoTextNode, currentNodePosX + 1, currentNodePosY - 2)  #Move to new position
    else:
        flow.SetPos(annoTextNode, currentNodePosX, currentNodePosY - 3)  #Move new merge to new position    
    mergeNode.Background = sortedPaintList[tool].Output  #Link all nodes
    mergeNode.Foreground = annoTextNode.Output
    if scriptParams['takeScreenshot'] == 1:
        rendJpeg = comp.Saver()
        rendName = os.path.dirname(comp.GetAttrs("COMPS_FileName")) + "\\Cam_" + str(cameraList[int(scriptParams['cameraSelect'])]) + "\\cam" + str(cameraList[int(scriptParams['cameraSelect'])]) + "_anno_" + str(annoNum-1) + "_.jpg"
        rendJpeg.SetInput("Clip", rendName)
        rendJpeg.SetInput("OutputFormat", "JpegFormat")
        rendJpeg.ConnectInput("Input", mergeNode)
        renderRes = comp.Render({"Start": refFrame,"End": refFrame, "Tool": rendJpeg, "SizeType": 1, "Wait": True})
        rendJpeg.Delete()

comp.Unlock()
comp.EndUndo(True) #End undo loop
print(exportData)
if scriptParams['writeFile'] == 1:        #If Write to file checkbox is set - open file an write data
    fileName = os.path.dirname(comp.GetAttrs("COMPS_FileName")) + "\\cam_" + str(cameraList[int(scriptParams['cameraSelect'])]) + ".txt"  #Generate path and filename
    with open(fileName,'a') as f:
        f.write(exportData)