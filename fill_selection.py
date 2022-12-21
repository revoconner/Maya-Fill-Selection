import pymel.core as pm
import maya.cmds as cmds
import re

loop_flag = "True"
# Get a list of the selected faces
selected_faces = pm.ls(sl=True, fl=True)

#get the name of parent mesh
parent_mesh = pm.PyNode(selected_faces[0].node().getParent())
#get total face so as to iterate later to grow selection
total_faces = cmds.polyEvaluate( str(parent_mesh), f=True)


#getting a list of ordered faces and removing the last face from the loop_faces
orderedSelection = cmds.ls( orderedSelection=True)
len_orderedSelection = len(orderedSelection)

#storing last face here
lastface = orderedSelection[len_orderedSelection-1]
#getting a list of ordered faces and removing the last face from the loop_faces
match = re.search(r'\[(\d+)\]', str(lastface))
if match:
    lastface_id = int(match.group(1))
else:
    number = None

loop_faces = []
for items in selected_faces:
	loop_faces.append(items)
	if str(lastface_id) in str(items):
		loop_faces.remove(items)

		
#checking if loop is complete

for faces in loop_faces:
	#checking adjacent faces 
	connected_faces = faces.connectedFaces()
		
	
	#check for triangle
	if ":" in str(connected_faces):
		face_string = str(connected_faces)
		# Use the re.finditer function to extract the face indices
		face_indices = [match.group() for match in re.finditer(r'\d+', face_string)]
		# Create a list of strings by iterating over the face indices
		face_strings = ['{}.f[{}]'.format(face_string.split('.')[0], index) for index in face_indices]
		tri_CF_Countr = 0		
		for face_string in face_strings:	
			if len(pm.ls(face_string, sl=True)) >= 1:
				tri_CF_Countr = tri_CF_Countr+1
			
	else:
		#for face with no adjacent triangles
		cFaces_length = len(pm.ls(connected_faces, sl=True))
		
		#checking for both quads and triangles
		if cFaces_length < 2:
			loop_flag = "False"
			if tri_CF_Countr < 1:
				loop_flag = "False"
				
		
print(loop_flag)

#delete this segment later
#print(loop_faces)
#print(lastface)
#print(selected_faces)


#splitting into multiple shell
pm.polySplitEdge(loop_faces)

#selecting inside faces
pm.select(lastface)
grow = 0 
while grow <= total_faces:
	mel.eval('PolySelectTraverse 1')
	grow= grow+1
pm.select(loop_faces, add=True)
	
#deleteing polySplitEdge node to make the mesh whole again	
hist = cmds.listHistory(str(parent_mesh))
outMesh = str(hist[2])+".outMesh"
inMesh = str(hist[0])+".inMesh"

cmds.connectAttr(outMesh, inMesh, force=True)
