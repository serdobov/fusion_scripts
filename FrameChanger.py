from pprint import pprint
initDialog = {}
unsortedToolFrameList = []
tool = comp.ActiveTool
dump = tool.SaveSettings() #Get all settings from node as dict.
for toolstruct in dump['Tools']:
    if "Multi" in toolstruct:  #Find all "Multistroke" keys
        for strokelist in dump['Tools'][toolstruct]:
            if "Strok" in strokelist: # Find all Strokes in each Multistroke
                for stroke in dump['Tools'][toolstruct][strokelist]:
                    unsortedToolFrameList.append(int(dump['Tools'][toolstruct][strokelist][stroke]['Time']))
                    #
toolFrameList = list(set(unsortedToolFrameList))    #Remove duplicated frame numbers
toolFrameList.sort() #Sort frame numbers
toolframeListIndex = len(toolFrameList)
for frameIndex in range(len(toolFrameList)):
    frameName = "Frame: " + str(toolFrameList[frameIndex])
    initDialog[frameIndex + 1] = {1: frameName, "Name": toolFrameList[frameIndex], 2: "Checkbox", "Default": 1} 
    #initDialog[frameIndex] = {1: "t_" + str(frameIndex), "Name": str(dump['Tools'][toolstruct][strokelist][stroke]['Time']), 2: "Checkbox", "Default": 1} 
pprint(initDialog)
selection = comp.AskUser("Keyframes", initDialog)
pprint(selection)
