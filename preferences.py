import bpy

class AntonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):

        import importlib
        from .utils_pip import Pip
        Pip._ensure_user_site_package()

        layout = self.layout
        flag = importlib.util.find_spec('regex') is not None and importlib.util.find_spec('tqdm') is not None
        if flag:
            layout.label(text='Regex and Tqdm loaded.', icon='INFO')
        else:
            layout.label(text='anton requires Regex and Tqdm!', icon='ERROR')
            row = layout.row()
            row.operator('anton.installer')

class AntonInstaller(bpy.types.Operator):
    bl_idname = "anton.installer"
    bl_label = "Install Regex and Tqdm"
    bl_description = ("Install Regex and Tqdm")

    def execute(self, context):
        try:
            from .utils_pip import Pip
            # Pip.upgrade_pip()
            Pip.install('regex')
            Pip.install('tqdm')

            import re
            from tqdm import tqdm

            for _ in tqdm(range(1)):
                print(re.__version__)

            self.report({'INFO'}, 'Successfully installed Re and Tqdm.')
        except ModuleNotFoundError:
            self.report({'ERROR'}, 'Could not install Regex and Tqdm, Kindly install it manually.')
        return {'FINISHED'}