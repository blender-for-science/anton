import bpy
import numpy as np
import os

class Anton_OT_ForceUpdater(bpy.types.Operator):
    bl_idname = "anton.forceupdate"
    bl_label = ""

    diffuse_library = [
                        (255/255, 0/255, 199/255, 1),
                        (255/255, 248/255, 0/255, 1),
                        (83/255, 255/255, 0/255, 1),
                        (13/255, 218/255, 134/255, 1),
                        (115/255, 255/255, 0/255, 1),
                        (0/255, 217/255, 255/255, 1),
                        (235/255, 255/255, 0/255, 1),
                        (255/255, 178/255, 83/255, 1),
                        (148/255, 13/255, 88/255, 1),
                        (255/255, 0/255, 141/255, 1),
                        (255/255, 139/255, 0/255, 1)]

    def execute(self, context):
        """Adds ``NATIVE``, ``FIXED``, ``NODESIGNSPACE`` and ``FORCE_{}`` materials and
        vertex groups ``DIRECTION_{}`` to the active object to facilitate problem definition.

        :return: ``FINISHED`` if successful, ``CANCELLED`` otherwise

        \\
        """
        scene = context.scene
        active_object = bpy.context.active_object
        
        bpy.ops.anton.initialize()

        if scene.anton.initialized:
            if 'NATIVE' not in bpy.data.materials:
                native_mat = bpy.data.materials.new(name='NATIVE')
                active_object.data.materials.append(native_mat)

            if 'FIXED' not in bpy.data.materials:
                mat = bpy.data.materials.new(name='FIXED')
                mat.diffuse_color = (1, 0, 0, 1)
                active_object.data.materials.append(mat)

            if 'NONDESIGNSPACE' not in bpy.data.materials:
                nds_mat = bpy.data.materials.new(name='NONDESIGNSPACE')
                nds_mat.diffuse_color = (0, 0, 1, 1)
                active_object.data.materials.append(nds_mat)

            for i in range(scene.anton.number_of_forces):
                if str('FORCE_{}'.format(i+1)) not in bpy.data.materials:

                    # Take care of popping of excess forces
                    size = len(scene.forceprop)
                    new = scene.forceprop.add()
                    new.name = str(size+1)
                    new.direction_boolean = False

                    temp_mat = bpy.data.materials.new(name='FORCE_{}'.format(i+1))
                    temp_mat.diffuse_color = self.diffuse_library[i]
                    active_object.data.materials.append(temp_mat)

                    bpy.ops.object.vertex_group_add()
                    active_object.vertex_groups.active.name = 'DIRECTION_{}'.format(i+1)

            scene.anton.forced = True
            self.report({'INFO'}, 'FORCES: {}'.format(scene.anton.number_of_forces))
            return{'FINISHED'}

        else:
            self.report({'ERROR'}, 'Initialize before problem definition.')
            return{'CANCELLED'}

class Anton_OT_Initializer(bpy.types.Operator):
    bl_idname = 'anton.initialize'
    bl_label = 'Anton_Initializer'
    bl_description = 'Initializes design space'

    def execute(self, context):
        """Design space is defined with existing geometry. 

        :ivar objects: List of all the obstacle objects
        :vartype objects: ``list``
        :ivar points: Bounding points of all the obstacles
        :vartype points: numpy array of ``floats``
        :ivar hull: Convexhull of the bounding points
        :vartype hull: numpy array of ``floats``

        :return: ``FINISHED`` if successful, ``CANCELLED`` otherwise
        """
        scene = context.scene
        active_object = bpy.context.active_object
        bpy.context.space_data.shading.type = 'MATERIAL'

        if not scene.anton.defined:
            scene.anton.filename = active_object.name

            if not os.path.exists(os.path.join(scene.anton.workspace_path, scene.anton.filename)):
                os.makedirs(os.path.join(scene.anton.workspace_path, scene.anton.filename))

            # subprocess.call(["python3", os.path.join(scene.anton.taichi_path, "projects/spgrid_topo_opt/scripts/opt_anton.py")])

            bpy.ops.object.modifier_add(type='TRIANGULATE')
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Triangulate")
            bpy.ops.export_scene.obj(filepath=os.path.join(scene.anton.workspace_path, scene.anton.filename, scene.anton.filename + '.obj'), 
                                        check_existing=True,
                                        axis_forward='Y',
                                        axis_up='Z',
                                        filter_glob="*.obj;*.mtl",
                                        use_selection=False,
                                        use_animation=False,
                                        use_mesh_modifiers=True,
                                        use_normals=False,
                                        use_uvs=False,
                                        use_materials=False,
                                        use_triangles=True,
                                        use_nurbs=False,
                                        use_vertex_groups=False,
                                        use_blen_objects=True,
                                        group_by_object=False,
                                        group_by_material=False,
                                        keep_vertex_order=True,
                                        global_scale=1, path_mode='AUTO')

            scene.anton.initialized = True
            self.report({'INFO'}, 'Initialized design space.')
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, 'Design space has already been initialized. In order to re-initialize, kindly restart the process.')
            return {'CANCELLED'}