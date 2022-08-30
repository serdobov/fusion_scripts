paintList = comp.GetToolList(True, "Paint")
for tool in paintList:
    dump = paintList[tool].SaveSettings() #Get all settings from node as dict.
    comment = paintList[tool].GetInput("Comments")  #Get Comments field value. Used for keeping annotated object name
    unsortedToolFrameList = []
    for toolstruct in dump['Tools']:
        if "Multi" in toolstruct:  #Find all "Multistroke" keys
            for strokelist in dump['Tools'][toolstruct]:
                if "Strok" in strokelist: # Find all Strokes in each Multistroke
                    for stroke in dump['Tools'][toolstruct][strokelist]:
                        unsortedToolFrameList.append(int(dump['Tools'][toolstruct][strokelist][stroke]['Time'])) 
    toolFrameList = list(set(unsortedToolFrameList))
    toolFrameList.sort() #Sort frame numbers
    frameListLen = len(toolFrameList)
    comp.Lock()
    if frameListLen == 3:
        rendJpeg = comp.Saver()
        rendName = "D:\\Projects\\FusionTests\\" + paintList[tool].Name + ".jpg"
        rendJpeg.SetInput("Clip", rendName)
        rendJpeg.SetInput("OutputFormat", "JpegFormat")
        rendJpeg.ConnectInput("Input", paintList[tool])
        # paintList[tool].Output = rendJpeg.Input
        renderRes = comp.Render({"Start": toolFrameList[1],"End": toolFrameList[1], "Tool": rendJpeg, "SizeType": 2, "Wait": True})
        rendJpeg.Delete()
    elif frameListLen == 2:
        rendJpeg = comp.Saver()
        rendName = "D:\\Projects\\FusionTests\\" + paintList[tool].Name + ".jpg"
        rendJpeg.SetInput("Clip", rendName)
        rendJpeg.SetInput("OutputFormat", "JpegFormat")
        rendJpeg.ConnectInput("Input", paintList[tool])
        #paintList[tool].Output = rendJpeg.Input
        renderRes = comp.Render({"Start": toolFrameList[1],"End": toolFrameList[1], "Tool": rendJpeg, "SizeType": 2, "Flags": 262144, "Wait": True})
        rendJpeg.Delete()      
    else:
        print("NoFrames to render.")
    comp.Unlock()