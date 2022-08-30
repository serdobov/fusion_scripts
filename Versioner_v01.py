import re

try:
    tool = comp.ActiveTool()
except:
    print("Error: You need to select a Loader.")
    exit()
if tool.GetAttrs("TOOLS_RegID") == "Loader":
    sourcePath = tool.GetInput("Clip")
    if sourcePath == "":
        print("You need to set path to souce plate.")
        exit()
    versionFind = re.search('[Vv]\d+', sourcePath)
    #versionNumber = re.search('\d+', versionFind.group())
    comp.Lock()
    allSavers = comp.GetToolList(False, "Saver")
    for currentSaver in allSavers:
        currentSaverPath = allSavers[currentSaver].GetInput("Clip")
        newSaverPath = re.sub('[Vv]\d+', versionFind.group(), currentSaverPath)
        allSavers[currentSaver].SetInput("Clip", newSaverPath)
        print(currentSaverPath + ' -> ' + newSaverPath)
    print (str(len(allSavers)) + " entries changed successfully.")
    oldCompPath = comp.GetAttrs("COMPS_FileName")
    newCompPath = re.sub('[Vv]\d+', versionFind.group(), oldCompPath)
    comp.Unlock()
    try:
        comp.Save(newCompPath)
        print("Comp " + newCompPath + " saved successfully.")
    except:
        print("Error: can't save new composition version.")    
else:
    print("This is not a Loader!")

