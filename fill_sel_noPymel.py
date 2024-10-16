import maya.cmds as cmds
import re

loop_flag = "True"
# Get a list of the selected faces
selected_faces = cmds.ls(sl=True, fl=True)

# Get the name of the parent mesh
parent_mesh = cmds.listRelatives(selected_faces[0].split('.')[0], parent=True)[0]
# Get total face count to iterate later to grow selection
total_faces = cmds.polyEvaluate(parent_mesh, f=True)

# Getting a list of ordered faces and removing the last face from loop_faces
orderedSelection = cmds.ls(orderedSelection=True)
len_orderedSelection = len(orderedSelection)

# Storing last face here
lastface = orderedSelection[len_orderedSelection-1]
# Extracting the face ID from the last face
match = re.search(r'\[(\d+)\]', str(lastface))
if match:
    lastface_id = int(match.group(1))

loop_faces = []
for face in selected_faces:
    loop_faces.append(face)
    if str(lastface_id) in face:
        loop_faces.remove(face)

# Checking if loop is complete
for face in loop_faces:
    # Checking adjacent faces
    connected_faces = cmds.polyListComponentConversion(face, ff=True, toFace=True)
    connected_faces = cmds.filterExpand(connected_faces, sm=34)

    # Check for triangle
    if connected_faces:
        tri_CF_Countr = 0
        for connected_face in connected_faces:
            if len(cmds.ls(connected_face)) >= 1:
                tri_CF_Countr += 1
    else:
        # For face with no adjacent triangles
        if len(connected_faces) < 2:
            loop_flag = "False"
            if tri_CF_Countr < 1:
                loop_flag = "False"

print(loop_flag)

# Splitting into multiple shell
cmds.polySplitEdge(loop_faces)

# Selecting inside faces
cmds.select(lastface)
grow = 0
while grow <= total_faces / 4:  # Growing selection in multiples of 4
    cmds.mel.eval('PolySelectTraverse 1')
    grow += 1
cmds.select(loop_faces, add=True)

# Deleting polySplitEdge node to make the mesh whole again
hist = cmds.listHistory(parent_mesh)
outMesh = hist[2] + ".outMesh"
inMesh = hist[0] + ".inMesh"

cmds.connectAttr(outMesh, inMesh, force=True)
