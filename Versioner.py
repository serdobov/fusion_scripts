# The script gets the version number of the path to the source 
# material in the loader and updates the version in the names 
# of the composition and all savers inside the script. To work, 
# make the loader with the source material active and run the 
# script from the menu.

import re
from pathlib import Path, PurePath

try:
    tool = comp.ActiveTool()  #Check that some tool is selected.
except:
    print("Error: You need to select a Loader.")
    exit()
if tool.GetAttrs("TOOLS_RegID") == "Loader": #Check that selected tool is Loader
    sourcePath = Path(tool.GetInput("Clip")) # Get path from lodaer
    globalIn = tool.GetInput("GlobalIn")  # Get loader start frame (probably 0, but who knows...)
    globalOut = tool.GetInput("GlobalOut") # Get loader end frame
    if comp.GetAttrs("COMPN_GlobalStart") != globalIn: # Check that comp IN equal source IN 
        comp.SetAttrs({"COMPN_GlobalStart":globalIn})  # Change if needed
        comp.SetAttrs({"COMPN_RenderStart":globalIn})
    if comp.GetAttrs("COMPN_GlobalEnd") != globalOut:  #Check thah comp OUT equal source OUT
        comp.SetAttrs({"COMPN_GlobalEnd":globalOut})  # and change if needed
        comp.SetAttrs({"COMPN_RenderEnd":globalOut})
    if sourcePath == "":
        print("You need to set path to souce plate.")
        exit()
    versionFind = re.search('[Vv]\d+', str(sourcePath))   # Parse version number from path
    comp.Lock()
    allSavers = comp.GetToolList(False, "Saver")  # Get all Savers from current comp
    for currentSaver in allSavers:  # Evaluate thru all Savers one by one
        currentSaverPath = Path(allSavers[currentSaver].GetInput("Clip"))   # Get path from current Saver
        newSaverPath = Path(re.sub('[Vv]\d+', versionFind.group(), str(currentSaverPath)))  # Replace version token in path for a new version
        allSavers[currentSaver].SetInput("Clip", str(newSaverPath))  # Set new path in current Saver node
        print(str(currentSaverPath) + ' -> ' + str(newSaverPath))
    print (str(len(allSavers)) + " entries changed successfully.")
    oldCompPath = Path(comp.GetAttrs("COMPS_FileName"))  # Get current comp file path
    newCompPath = re.sub('[Vv]\d+', versionFind.group(), str(oldCompPath)) # Replace version 
    comp.Unlock()
    try:
        comp.Save(str(newCompPath))    # Save current comp tith new name
        print("Comp " + str(newCompPath) + " saved successfully.")
    except:
        print("Error: can't save new composition version.")    
else:
    print("This is not a Loader!")

