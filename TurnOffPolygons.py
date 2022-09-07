polygons = comp.GetToolList(False, "PolylineMask")
for polyItem in polygons:
    polygons[polyItem].SetAttrs({"TOOLB_PassThrough":True})