from collections import OrderedDict
import bpy
import numpy as np
import os

def get_grease_pencil(gpencil_obj_name='GPencil') -> bpy.types.GreasePencil:
    if gpencil_obj_name not in bpy.context.scene.objects:
        bpy.ops.object.gpencil_add(location=(0, 0, 0), type='EMPTY')
        bpy.data.grease_pencils['GPencil'].name = gpencil_obj_name
        bpy.context.scene.objects[-1].name = gpencil_obj_name

    gpencil = bpy.context.scene.objects[gpencil_obj_name]
    gp_mat = bpy.data.materials.new('GP')
    bpy.data.materials.create_gpencil_data(gp_mat)
    gp_mat.grease_pencil.color = bpy.data.materials[gpencil_obj_name].diffuse_color[:]

    bpy.data.grease_pencils[gpencil_obj_name].materials.append(gp_mat)
    gpencil.hide_select = True

    return gpencil

def get_grease_pencil_layer(gpencil: bpy.types.GreasePencil, gpencil_layer_name='GP_Layer',
                            clear_layer=False) -> bpy.types.GPencilLayer:

    if gpencil.data.layers and gpencil_layer_name in gpencil.data.layers:
        gpencil_layer = gpencil.data.layers[gpencil_layer_name]
    else:
        gpencil_layer = gpencil.data.layers.new(gpencil_layer_name, set_active=True)

    if clear_layer:
        gpencil_layer.clear()

    return gpencil_layer

def init_grease_pencil(gpencil_obj_name='GPencil', gpencil_layer_name='Annotation_Layer',
                       clear_layer=True) -> bpy.types.GPencilLayer:
    gpencil = get_grease_pencil(gpencil_obj_name)
    gpencil_layer = get_grease_pencil_layer(gpencil, gpencil_layer_name, clear_layer=clear_layer)
    return gpencil_layer

def draw_arrow(gp_frame, p: tuple, norm: tuple, d: tuple, size: int, reverse: bool):
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'

    orient = np.sign(np.dot(np.array(norm), np.array(d)))

    t = tuple(np.array(p) + orient * size * np.array(d))
    norm_d = np.array((d[1], -1*d[0], 0))

    if np.abs(np.dot(d, norm_d)) > 0:
        norm_d = np.array((0, -1*d[2], d[1]))
    elif np.linalg.norm(norm_d) == 0:
        norm_d = np.array((0, 1, 0))

    if reverse:
        start = t
        end = tuple(np.array(p) + 0.15 * orient * np.array(d))
        sign = 1.0
    else:
        start = p
        end = t
        sign = -1.0

    arrow_left = tuple(np.array(end) + 0.1 * norm_d)
    arrow_top = tuple(np.array(end) - sign * orient * 0.1 * np.array(d))
    arrow_right = tuple(np.array(end) - 0.1 * norm_d)

    gp_stroke.points.add(count=5)
    gp_stroke.points[0].co = start
    gp_stroke.points[1].co = end
    gp_stroke.points[2].co = arrow_left
    gp_stroke.points[3].co = arrow_top
    gp_stroke.points[4].co = arrow_right

    return gp_stroke

class Anton_OT_DirectionUpdater(bpy.types.Operator):
    bl_idname = "anton.directionupdate"
    bl_label = ""
    bl_description = 'Changes direction sign'

    force_id : bpy.props.StringProperty()
    direction_reverse = OrderedDict()

    def execute(self, context):
        """Instantiates an arrow at the centroid of a face on which force is applied. The instantiated arrow is
        a grease pencil object whose color corresponds to the applied force. Arrow head flips when direction sign is changed.

        :return: ``FINISHED`` if successful, ``CANCELLED`` otherwise
        """
        scene = context.scene
        active_object = bpy.data.objects[scene.anton.filename]
        direction = np.array([0.0, 0.0, 0.0])
        face_indices = []

        if self.force_id not in self.direction_reverse.keys():
            self.direction_reverse[self.force_id] = True
        else:
            self.direction_reverse[self.force_id] = not self.direction_reverse[self.force_id]

        if self.direction_reverse[self.force_id]:
            scene.forced_direction_signs[self.force_id] = 1.0
        else:
            scene.forced_direction_signs[self.force_id] = -1.0

        if bpy.context.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        bpy.ops.mesh.select_all(action = 'DESELECT')

        active_object.vertex_groups.active_index = active_object.vertex_groups['DIRECTION_{}'.format(str(self.force_id).split('_')[-1])].index
        bpy.ops.object.vertex_group_select()

        bpy.ops.object.mode_set(mode='OBJECT')

        for edge in active_object.data.edges:
            if edge.select:
                vertices = active_object.data.edges[edge.index].vertices[:]
                vec = np.array(active_object.data.vertices[vertices[0]].co[:]) - np.array(active_object.data.vertices[vertices[1]].co[:])
                vec_mag = np.linalg.norm(vec)
                direction = vec/vec_mag
                break

        bpy.ops.object.mode_set(mode='OBJECT')
        centroids = list()
        normals = list()

        for face in active_object.data.polygons:
            if 'FORCE' in active_object.data.materials[face.material_index].name_full:
                if str(active_object.data.materials[face.material_index].name_full) == self.force_id:
                    face_indices.append(face.index)

                    centroid = (1/3) * (np.array(active_object.data.vertices[face.vertices[0]].co) \
                                 + np.array(active_object.data.vertices[face.vertices[1]].co) \
                                  + np.array(active_object.data.vertices[face.vertices[2]].co))

                    centroids.append(centroid)
                    normals.append(face.normal)


        if len(centroids) > 0 and np.linalg.norm(direction) > 0:

            gp_layer = init_grease_pencil(gpencil_obj_name=self.force_id)
            gp_frame = gp_layer.frames.new(0)
            strokes = []

            #CAPPED DIRECTION ARROWS AT 10 PER FORCE
            for i, point in enumerate(centroids):
                if i<10:
                    norm = normals[i]
                    strokes.append(gp_frame.strokes.new())
                    strokes[-1] = draw_arrow(gp_frame, point, norm, tuple(direction), 1, self.direction_reverse[self.force_id])
                    strokes[-1].line_width = 50
                else:
                    break

            bpy.ops.object.select_all(action = 'DESELECT')
            bpy.context.view_layer.objects.active = active_object

            scene.anton.force_directioned = True
            self.report({'INFO'}, '{}: Magnitude: {}, Face(s): {}, Direction: {}'.format(
                                                                        self.force_id,
                                                                        scene.forced_magnitudes[self.force_id],
                                                                        face_indices,
                                                                        scene.forced_direction_signs[self.force_id]))
            return{'FINISHED'}

        else:
            if len(centroids) > 0:
                self.report({'ERROR'}, 'Assign direction to each specified force with vertex groups.')
            else:
                self.report({'ERROR'}, 'Assign face(s) to each specified force.')

            scene.anton.force_directioned = False
            return{'CANCELLED'}

class Anton_OT_Definer(bpy.types.Operator):
    bl_idname = 'anton.define'
    bl_label = 'Anton_Definer'
    bl_description = 'Defines the problem'

    def execute(self, context):
        """Defines the problem after creation of a tetrahedral finite element mesh and stores
        the mesh variables as a binary numpy file which is accessed by ``Anton_OT_Processor``

        :ivar nodes: Cartesian position of nodes
        :vartype nodes: *numpy.array* of ``float``
        :ivar elements: Connectivity array of nodes
        :vartype elements: *numpy.array* of ``int``
        :ivar fixed_nodes: Indices of fixed nodes
        :vartype fixed_nodes: *numpy.array* of ``int``
        :ivar non_design_nodes: Indices of non-design nodes
        :vartype non_design_nodes: *numpy.array* of ``int``
        :ivar forced_nodes: Indices of forced nodes
        :vartype forced_nodes: *numpy.array* of ``int``
        :ivar directions: Direction vector corresponding to each force
        :vartype directions: ``dict``
        :ivar distributed_force: Magnitude per area of each force
        :vartype distributed_force: ``dict``

        :return: ``FINISHED`` if successful, ``CANCELLED`` otherwise

        \\
        """
        scene = context.scene
        active_object = bpy.data.objects[scene.anton.filename]

        fixed_faces = []
        non_design_faces = []
        forced_faces = OrderedDict()
        forced_directions = []

        if scene.anton.force_directioned:
            bpy.ops.object.mode_set(mode='OBJECT')
            for face in active_object.data.polygons:
                if 'FIXED' in active_object.data.materials[face.material_index].name_full:
                    coords = []
                    for _vertex_id in active_object.data.polygons[face.index].vertices[:]:
                        coords.append(active_object.data.vertices[_vertex_id].co[:])

                    fixed_faces.append(coords)

                elif 'NONDESIGNSPACE' in active_object.data.materials[face.material_index].name_full:
                    coords = []
                    for _vertex_id in active_object.data.polygons[face.index].vertices[:]:
                        coords.append(active_object.data.vertices[_vertex_id].co[:])

                    non_design_faces.append(coords)

                elif 'FORCE' in active_object.data.materials[face.material_index].name_full:
                    force_id = str(active_object.data.materials[face.material_index].name_full)
                    coords = []
                    for _vertex_id in active_object.data.polygons[face.index].vertices[:]:
                        coords.append(active_object.data.vertices[_vertex_id].co[:])

                    if force_id not in forced_faces.keys():
                        forced_faces[force_id] = [coords]
                    else:
                        forced_faces[force_id].append(coords)

            if bpy.context.mode != 'EDIT':
                bpy.ops.object.mode_set(mode='EDIT')

            for i in range(scene.anton.number_of_forces):
                bpy.ops.mesh.select_all(action = 'DESELECT')

                active_object.vertex_groups.active_index = active_object.vertex_groups['DIRECTION_{}'.format(i+1)].index
                bpy.ops.object.vertex_group_select()

                bpy.ops.object.mode_set(mode='OBJECT')

                for edge in active_object.data.edges:
                    if edge.select:
                        coords = []
                        for _vertex_id in active_object.data.edges[edge.index].vertices[:]:
                            coords.append(active_object.data.vertices[_vertex_id].co[:])

                        forced_directions.append(self.compute_direction(coords))

                bpy.ops.object.mode_set(mode='EDIT')

            bpy.ops.object.mode_set(mode='OBJECT')

            forces = []
            force_vectors = []
            for i, _force_id in enumerate(forced_faces):
                forces.append(forced_faces[_force_id])
                force_vectors.append(scene.forced_magnitudes[_force_id] * scene.forced_direction_signs[_force_id] * forced_directions[i])

            print(np.array(forces), np.array(force_vectors))

            self.report({'INFO'}, 'Fixed: {}, Non Design Space: {}, Force: {}'.format(
                                                                                len(fixed_faces),
                                                                                len(non_design_faces),
                                                                                len(forced_faces)))

            scene.anton.defined = True
            return {'FINISHED'}

        else:
            scene.anton.defined = False
            self.report({'ERROR'}, 'Problem ill-defined')
            return {'CANCELLED'}


    def create_geo(self,
                    path,
                    filename,
                    fixed_faces,
                    non_design_faces,
                    forced_faces,
                    forced_magnitudes,
                    forced_directions,
                    forced_direction_signs,
                    geo_points,
                    geo_edges,
                    points,
                    edges,
                    curve_loop,
                    clmax):

        """Creates a tetrahedral finite element mesh of the object with **gmsh_api**, adds physical groups for fixed, forced and non-design space faces
        and retrieves direction of each applied force from assigned vertex groups.

        :param path: Workspace path
        :type path: ``str``
        :param filename: Name of the initialized object
        :type filename: ``str``

        :param fixed_faces: Indices of fixed faces
        :type fixed_faces: ``set``
        :param non_design_faces: Indices of non-design space faces
        :type non_design_faces: ``set``
        :param forced_faces: Indices of faces corresponding to each force
        :type forced_faces: ``dict``
        :param forced_magnitudes:  Magnitude of each force
        :type forced_magnitudes: ``dict``

        :param forced_directions: Direction of each force
        :type forced_directions: ``dict``
        :param forced_direction_signs: Direction sign of each force
        :type forced_direction_signs: ``dict``

        :param curve_loop: Connectivity of each triangle of the object
        :type curve_loop: ``dict``

        :param geo_points: Vertices of the object
        :type geo_points: ``dict``
        :param geo_edges: Edges of the object
        :type geo_edges: ``dict``

        :param clmax: Maximum element size
        :type clmax: ``float``

        :return: ``nodes``, ``elements``, ``fixed_nodes``, ``non_design_nodes``, ``forced_nodes``, ``directions``, ``distributed_force``
        """

        import gmsh_api.gmsh as gmsh

        geo = gmsh.model.geo
        lc = clmax

        directions = OrderedDict()
        force_per_areas = OrderedDict()
        distributed_force = OrderedDict()

        all_forced_faces = set()
        for _face_lists in forced_faces.values():
            for _face_id in _face_lists:
                all_forced_faces.add(_face_id)

        for _point in points.keys():
            geo.addPoint(_point[0], _point[1], _point[2], lc, points[_point])

        for _edge in edges.keys():
            geo.addLine(_edge[0], _edge[1], edges[_edge])

        for _force_id in forced_directions.keys():
            forced_edge = geo_edges[forced_directions[_force_id]]
            forced_vertices = []
            for _vertex_id in forced_edge:
                forced_vertices.append(geo_points[_vertex_id])

            if _force_id in forced_direction_signs.keys():
                directions[_force_id] = forced_direction_signs[_force_id] * self.compute_direction(forced_vertices)
            else:
                directions[_force_id] = self.compute_direction(forced_vertices)


        for _curve_id in curve_loop.keys():
            geo.addCurveLoop([curve_loop[_curve_id][0], curve_loop[_curve_id][1], curve_loop[_curve_id][2]], _curve_id)
            surf_temp = geo.addPlaneSurface([_curve_id], _curve_id)

            if _curve_id in fixed_faces:
                gmsh.model.addPhysicalGroup(2, [surf_temp], _curve_id)

            elif _curve_id in non_design_faces:
                gmsh.model.addPhysicalGroup(2, [surf_temp], _curve_id)

            elif _curve_id in all_forced_faces:
                gmsh.model.addPhysicalGroup(2, [surf_temp], _curve_id)

        for _force_id in forced_faces.keys():
            force_per_areas[_force_id] = []
            for _face_id in forced_faces[_force_id]:
                temp_vertex_ids = set()
                temp_vertices = []

                for _edge_id in np.abs(curve_loop[_face_id]):
                    for _point_id in geo_edges[_edge_id]:
                        temp_vertex_ids.add(_point_id)

                for _vertex_id in temp_vertex_ids:
                    temp_vertices.append(np.array(geo_points[_vertex_id]))

                force_per_areas[_force_id].append(self.compute_area(temp_vertices))

        for _force_id in force_per_areas.keys():
            distributed_force[_force_id] = forced_magnitudes[_force_id]/np.sum(force_per_areas[_force_id])

        sl = geo.addSurfaceLoop(list(curve_loop.keys()))
        _ = geo.addVolume([sl])

        gmsh.model.geo.synchronize()
        gmsh.option.setNumber("Mesh.Algorithm", 0)
        gmsh.option.setNumber("Mesh.ElementOrder", 1)

        gmsh.option.setNumber("Mesh.Optimize", 1)
        gmsh.option.setNumber("Mesh.QualityType", 2)
        gmsh.option.setNumber("Mesh.SaveAll", 1)
        gmsh.model.mesh.generate(3)

        fixed_nodes = set()
        non_design_nodes = set()
        forced_nodes = OrderedDict()

        nodes = np.array(gmsh.model.mesh.getNodes()[1]).reshape(len(gmsh.model.mesh.getNodes()[0]), 3)
        elements = np.array(gmsh.model.mesh.getElements(3)[2][0], dtype=np.int).reshape(len(gmsh.model.mesh.getElements(3)[1][0]), 4) - 1

        for _face_id in fixed_faces:
            for _fixed_node_id in gmsh.model.mesh.getNodesForPhysicalGroup(2, _face_id)[0]:
                fixed_nodes.add(_fixed_node_id - 1)

        for _face_id in non_design_faces:
            for _non_design_node_id in gmsh.model.mesh.getNodesForPhysicalGroup(2, _face_id)[0]:
                non_design_nodes.add(_non_design_node_id - 1)

        for _force_id in forced_faces.keys():
            forced_nodes[_force_id] = []
            for _face_id in forced_faces[_force_id]:
                forced_nodes[_force_id].append([])
                # print(gmsh.model.mesh.getNodesForPhysicalGroup(2, _face_id)[0])
                for _forced_node_id in gmsh.model.mesh.getNodesForPhysicalGroup(2, _face_id)[0]:
                    forced_nodes[_force_id][-1].append(int(_forced_node_id - 1))

        gmsh.write(os.path.join(path, filename+'.msh'))
        return nodes, elements, fixed_nodes, non_design_nodes, forced_nodes, directions, distributed_force

    @staticmethod
    def get_curve_loop(surf):
        return [(surf[0], surf[1]), (surf[1], surf[2]), (surf[2], surf[0])]

    @staticmethod
    def get_edge_indices(surf):
        return [(surf[0], surf[2]), (surf[0], surf[1]), (surf[1], surf[2])]

    @staticmethod
    def get_raw_data(path):
        data = [[]]
        with open(path, 'r') as f:
            line = f.readline()
            while(line):
                if 'endfacet' in line:
                    data.append([])
                else:
                    if 'vertex' in line:
                        # Ignoring normals
                        data[-1].append(tuple(map(float, line[:-1].split(' ')[1:])))

                line = f.readline()

        return data[:-1]

    @staticmethod
    def compute_direction(points):
        vec = np.array(points[0]) - np.array(points[1])
        vec_mag = np.linalg.norm(vec)
        return vec/vec_mag

    @staticmethod
    def compute_area(points):
        v1 = points[1] - points[0]
        v2 = points[2] - points[0]
        v3 = np.cross(v1, v2)
        return 0.5 * np.linalg.norm(v3)




