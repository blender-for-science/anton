import bpy

class AntonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):

        import importlib
        from .utils_pip import Pip
        Pip._ensure_user_site_package()

        layout = self.layout
        deps = ['gmsh_api', 'tqdm', 'sklearn', 'scipy']

        flag = True
        for _module in deps:
            flag = flag and importlib.util.find_spec(_module) is not None

        if flag:
            layout.label(text='Loaded required modules.', icon='INFO')
        else:
            layout.label(text='anton requires few additional modules.', icon='ERROR')
            row = layout.row()
            row.operator('anton.installer')

class AntonInstaller(bpy.types.Operator):
    bl_idname = "anton.installer"
    bl_label = "Install required modules"
    bl_description = ("Installs required modules")

    def execute(self, context):
        try:
            from .utils_pip import Pip
            # Pip.upgrade_pip()
            Pip.install('tqdm')
            Pip.install('gmsh-api')
            Pip.install('scikit-learn')
            Pip.install('scipy')

            import gmsh_api
            from tqdm import tqdm
            import sklearn
            import scipy

            for _ in tqdm(range(1)):
                print("gmsh-api: ", gmsh_api.__version__)
                print("scikit-learn: ", sklearn.__version__)
                print("scipy: ", scipy.__version__)

            self.report({'INFO'}, 'Successfully installed required modules.')
        except ModuleNotFoundError:
            self.report({'ERROR'}, 'Could not install required modules, Kindly install them manually.')
        return {'FINISHED'}