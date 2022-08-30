# The script gets the version number of the path to the source 
# material in the loader and updates the version in the names 
# of the composition and all savers inside the script. To work, 
# make the loader with the source material active and run the 
# script from the menu.

import re

try:
    tool = comp.ActiveTool()  #Check that some tool is selected.
except:
    print("Error: You need to select a Loader.")
    exit()
if tool.GetAttrs("TOOLS_RegID") == "Loader": #Check that selected tool is Loader
    sourcePath = tool.GetInput("Clip") # Get path from lodaer
    if sourcePath == "":
        print("You need to set path to souce plate.")
        exit()
    versionFind = re.search('[Vv]\d+', sourcePath)   # Parse version number from path
    #versionNumber = re.search('\d+', versionFind.group())
    comp.Lock()
    allSavers = comp.GetToolList(False, "Saver")  # Get all Savers from current comp
    for currentSaver in allSavers:  # Evaluate thru all Savers one by one
        currentSaverPath = allSavers[currentSaver].GetInput("Clip")   # Get path from current Saver
        newSaverPath = re.sub('[Vv]\d+', versionFind.group(), currentSaverPath)  # Replace version token in path for a new version
        allSavers[currentSaver].SetInput("Clip", newSaverPath)  # Set new path in current Saver node
        print(currentSaverPath + ' -> ' + newSaverPath)
    print (str(len(allSavers)) + " entries changed successfully.")
    oldCompPath = comp.GetAttrs("COMPS_FileName")  # Get current comp file path
    newCompPath = re.sub('[Vv]\d+', versionFind.group(), oldCompPath) # Replace version 
    comp.Unlock()
    try:
        comp.Save(newCompPath)    # Save current comp tith new name
        print("Comp " + newCompPath + " saved successfully.")
    except:
        print("Error: can't save new composition version.")    
else:
    print("This is not a Loader!")

