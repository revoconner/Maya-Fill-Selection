## Better algorithm now, faster and works with verticesm edges and faces now


import maya.cmds as cmds
import maya.mel as mel

def get_component_type(component):
    if '.f[' in component:
        return 'face'
    elif '.e[' in component:
        return 'edge'
    elif '.vtx[' in component:
        return 'vertex'
    return None

def convert_to_faces(components):
    comp_type = get_component_type(components[0])
    if comp_type == 'face':
        return components
    elif comp_type == 'edge':
        faces = cmds.polyListComponentConversion(components, fe=True, tf=True)
    elif comp_type == 'vertex':
        faces = cmds.polyListComponentConversion(components, fv=True, tf=True)
    else:
        return components
    return cmds.filterExpand(faces, sm=34) or []

def get_adjacent_faces(face):
    edges = cmds.polyListComponentConversion(face, ff=True, te=True)
    edges = cmds.filterExpand(edges, sm=32) or []
    adjacent = cmds.polyListComponentConversion(edges, fe=True, tf=True)
    adjacent = cmds.filterExpand(adjacent, sm=34) or []
    return set(adjacent)

def flood_fill_faces(seed_face, boundary_faces):
    boundary_set = set(boundary_faces)
    visited = set()
    result = set()
    queue = [seed_face]

    while queue:
        current = queue.pop(0)
        if current in visited or current in boundary_set:
            continue
        visited.add(current)
        result.add(current)

        for adjacent in get_adjacent_faces(current):
            if adjacent not in visited and adjacent not in boundary_set:
                queue.append(adjacent)

    return list(result)

selected = cmds.ls(sl=True, fl=True)
ordered = cmds.ls(orderedSelection=True)

original_type = get_component_type(selected[0])

seed = ordered[-1]
boundary = [c for c in selected if c != seed]

seed_faces = convert_to_faces([seed])
boundary_faces = convert_to_faces(boundary)

if seed_faces:
    fill_faces = flood_fill_faces(seed_faces[0], boundary_faces)

    # Filter boundary to only faces adjacent to the fill
    fill_set = set(fill_faces)
    inner_boundary = []
    for bf in boundary_faces:
        adjacent = get_adjacent_faces(bf)
        if adjacent & fill_set:
            inner_boundary.append(bf)

    cmds.select(fill_faces + inner_boundary)

    if original_type == 'edge':
        mel.eval('ConvertSelectionToEdges')
    elif original_type == 'vertex':
        mel.eval('ConvertSelectionToVertices')
