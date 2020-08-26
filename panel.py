import bpy
from bpy.props import BoolVectorProperty

class Anton_PT_Panel(bpy.types.Panel):
    bl_idname = 'ANTON_PT_panel'
    bl_label = 'anton'
    bl_category = 'anton'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, 'workspace_path')

        row = layout.row()
        row.label(text=" ")

        row = layout.row(align=True)
        row.prop(scene.anton, "mode", icon='NONE', expand=True,
                    slider=True, toggle=False, icon_only=False, event=False,
                    full_event=False, emboss=True)

        row = layout.row()
        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, 'material')

        col = layout.column()
        col.operator('anton.initialize', text='Initialize')

        row = layout.row()
        row.label(text=" ")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, "number_of_forces")
        rowsub.operator('anton.forceupdate', icon='ADD')

        for item in scene.forceprop:
            row = layout.row()
            row.label(text=' ')
            row.prop(item, 'magnitude')
            scene.forced_magnitudes['FORCE_{}'.format(item.name)] = item.magnitude
            row.operator('anton.directionupdate', icon='FULLSCREEN_ENTER').force_id = 'FORCE_{}'.format(item.name)

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, "cl_max")

        col = layout.column()
        col.operator('anton.define', text='Define')

        row = layout.row()
        row.label(text=" ")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, "include_fixed")
        rowsub.label(text="")
        rowsub.prop(scene.anton, "include_forced")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, "number_of_neighbours")
        rowsub.prop(scene.anton, "rmin")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, "volumina_ratio")
        rowsub.prop(scene.anton, "penalty_exponent")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, "emin")
        rowsub.prop(scene.anton, "density_change")

        # row = layout.row(align=True)
        # row.prop(scene.anton, "filter_mode", icon='NONE', expand=True,
        #             slider=True, toggle=False, icon_only=False, event=False,
        #             full_event=False, emboss=True)

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, 'number_of_iterations')

        row = layout.row()
        row.label(text=" ")

        col = layout.column()
        col.operator('anton.process', text='Generate')

        row = layout.row()
        row.label(text=" ")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, "metaballrad")
        rowsub.prop(scene.anton, "metaballsens")
        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, 'keyframes')
        rowsub.prop(scene.anton, 'slices')

        rowsub = layout.row(align=True)
        rowsub.prop(scene.anton, 'viz_iteration')

        col = layout.column()
        col.operator('anton.visualize', text='Visualize')

        row = layout.row()
        row.label(text=" ")

        row = layout.row(align=True)
        row.alignment = 'RIGHT'
        row.label(text="Made with")
        row.label(icon='FUND')

