import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, EnumProperty, BoolProperty

class ForcePropertyGroup(bpy.types.PropertyGroup):
        """
        :ivar magnitude: Magnitude of the specified force (``1.0N``)
        :vartype magnitude: ``float``
        """

        magnitude : FloatProperty(
                                name="N",
                                default=1.0,
                                min=0.0,
                                precision=2,
                                description="Magnitude of the specified force")


class AntonPropertyGroup(bpy.types.PropertyGroup):
        """A class for dynamically defined sets of properties that are defined
        via **Anton_PT_Panel** and used across all the operator classes.

        :ivar initialized: Is the problem initialized?
        :vartype initialized: ``bool``
        :ivar forced: Forces acting on the object has been specified?
        :vartype forced: ``bool``
        :ivar force_directioned: Direction for each force has been specified?
        :vartype force_directioned: ``bool``
        :ivar defined: Is the problem well-defined?
        :vartype defined: ``bool``

        :ivar filename: Name of the active-object
        :vartype filename: ``str``
        :ivar workspace_path: Path to workspace folder (``/tmp/``)
        :vartype workspace_path: ``str``
        :ivar number_of_forces: Number of forces acting on the object (``1``)
        :vartype number_of_forces: ``int``

        :ivar include_fixed: Add fixed faces to non-design space? (``False``)
        :vartype include_fixed: ``bool``
        :ivar include_forced: Add forced faces to non-design space? (``False``)
        :vartype include_forced: ``bool``
        :ivar density_filter: Apply a smoothing filter on densities? (``False``)
        :vartype density_filter: ``bool``
        :ivar sensitivity_filter: Apply a smoothing filter to sensitivity? (``True``)
        :vartype sensitivity_filter: ``bool``

        :ivar cl_max: Maximum size of tetrahedral element (``0.2``)
        :vartype cl_max: ``float``
        :ivar rmin: Radius of neighbourhood (``0.2``)
        :vartype rmin: ``float``
        :ivar number_of_neighbours: Number of neighbours (``10``)
        :vartype number_of_neighbours: ``int``

        :ivar density_change: Change in density per iteration (``0.2``)
        :vartype density_change: ``float``
        :ivar emin: Minimum allowable value of Young's modulus (``1.0``)
        :vartype emin: ``float``

        :ivar metaballrad: Radius of metaballs (``0.2``)
        :vartype metaballrad: ``float``
        :ivar metaballsens: Sensitivity of metaballs (``0.7``)
        :vartype metaballsens: ``float``
        :ivar volumina_ratio: Ratio between the design space and solution space (``0.4``)
        :vartype volumina_ratio: ``float``
        :ivar penalty_exponent: Penalization factor for densities (``3.0``)
        :vartype penalty_exponent: ``float``

        :ivar number_of_iterations: Number of optimization iterations (``30``)
        :vartype number_of_iterations: ``int``
        :ivar viz_iteration: Which iteration to visualize? (``30``)
        :vartype viz_iteration: ``int``
        :ivar keyframes: Total number of keyframes (``30``)
        :vartype keyframes: ``int``
        :ivar slices: Number of instantiation points (``3``)
        :vartype slices: ``int``

        :ivar material: Material of the object (``PLA-Generic``)
        :vartype material: ``enum``

        \\
        """

        initialized : BoolProperty(default=False)
        optimized : BoolProperty(default=False)
        force_directioned : BoolProperty(default=False)
        defined : BoolProperty(default=False)

        filename : StringProperty()

        workspace_path : StringProperty(
                name="",
                description="Path to workspace folder",
                default='/tmp/',
                subtype='DIR_PATH')

        number_of_forces : IntProperty(
                name="Forces",
                default=1,
                min=1,
                description="Number of forces acting on the object")

        res : IntProperty(
                name="",
                default=100,
                min=10,
                description="Resolution")

        include_forced : BoolProperty(
                name='Forced',
                default=False,
                description='Adds forced faces to non-design space')

        include_fixed : BoolProperty(
                name='Fixed',
                default=False,
                description='Adds fixed faces to non-design space')

        advanced_params : BoolProperty(
                name='Advanced',
                default=False,
                description='Tweak advanced solver params')

        mode : EnumProperty(
                name='mode',
                items=[
                        ('NARROW', 'Narrow', 'Narrowband Topology optimization'),
                        ('WIREFRAME', 'Wire', 'Wireframe-Narrowband Topology optimization')],
                default='NARROW'
        )

        nds_density : FloatProperty(
                name="",
                default=0.1,
                min=0.0,
                max = 1.0,
                precision=2,
                description="Density of non-design space blocks")

        fixed_threshold : FloatProperty(
                name="",
                default=0.00001,
                min=0.0,
                max = 1.0,
                precision=6,
                description="Search threshold for fixed cells")

        forced_threshold : FloatProperty(
                name="",
                default=0.00001,
                min=0.0,
                max = 1.0,
                precision=6,
                description="Search threshold for forced nodes")

        wireframe_gridsize : IntProperty(
                name="",
                default=32,
                min=1,
                max=100,
                description="Grid size for wireframe")

        wireframe_thickness : IntProperty(
                name="",
                default=4,
                min=1,
                max=100,
                description="Thickness of wireframe")

        volumina_ratio : FloatProperty(
                name="",
                default=0.4,
                min=0.0,
                max=1.0,
                precision=3,
                description="Ratio between the design space and solution space")

        penalty_exponent : FloatProperty(
                name="",
                default=3.0,
                min=1.5,
                max = 15.0,
                precision=3,
                description="Penalization factor for densities")

        number_of_iterations : IntProperty(
                name="",
                default=30,
                min=1,
                description="Number of optimization iterations")

        viz_iteration : IntProperty(
                name="",
                default=30,
                min=1,
                description="Iteration to visualize")

        density_out : FloatProperty(
                name="",
                default=0.2,
                min=0.0,
                max=1.0,
                precision=2,
                description="Ratio between the design space and solution space")


        #ADVANCED PARAMS
        minimum_density : FloatProperty(
                name="",
                default=0.0,
                min=0.0,
                max=1.0,
                description="Minimum allowable density")

        minimum_stiffness : FloatProperty(
                name="",
                default=1e-9,
                min=0.0,
                max=1.0,
                description="Minimum allowable stiffness")

        fraction_to_keep : FloatProperty(
                name="",
                default=1.0,
                min=0.0,
                max=1.0,
                description="Fraction to keep during optimization")

        cg_tolerance : FloatProperty(
                name="",
                default=1e-4,
                min=0.0,
                max=1.0,
                description="CG Tolerance")

        active_threshold : FloatProperty(
                name="",
                default=1e-6,
                min=0.0,
                max=1.0,
                description="Active threshold")

        cg_max_iterations : IntProperty(
                name="",
                default=50,
                min=1,
                max=100,
                description="CG Max iterations")

        boundary_smoothing_iters : IntProperty(
                name="",
                default=3,
                min=1,
                max=100,
                description="Boundary smoothing iterations")

        smoothing_iters : IntProperty(
                name="",
                default=1,
                min=1,
                max=100,
                description="Interior smoothing iterations")

        objective_threshold : FloatProperty(
                name="",
                default=0.5,
                min=0.0,
                max=1.0,
                description="Objective threshold")

        step_limit : FloatProperty(
                name="",
                default=0.2,
                min=0.0,
                max=1.0,
                description="Step limit")

        exclude_fixed_cells : BoolProperty(
                name='Exclude Fixed-cells',
                default=True,
                description='Exclude fixed cells during optimization')

        material : EnumProperty(
                name='',
                items=[
                        ('Steel-28Mn6', 'Steel-28Mn6', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S690MC', 'Steel-S690MC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('PA6-Generic', 'PA6-Generic', 'Poisson ratio: 0.39, Youngs modulus: 2930.0 MPa'),
                        ('Steel-X39CrMo17-1', 'Steel-X39CrMo17-1', 'Poisson ratio: 0.3, Youngs modulus: 213000.0 MPa'),
                        ('Steel-S335N', 'Steel-S335N', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-3C22', 'Steel-3C22', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('PET-Generic', 'PET-Generic', 'Poisson ratio: 0.36, Youngs modulus: 3150.0 MPa'),
                        ('Steel-1C35', 'Steel-1C35', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-2C10', 'Steel-2C10', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJL-300', 'Steel-EN-GJL-300', 'Poisson ratio: 0.3, Youngs modulus: 125000.0 MPa'),
                        ('Steel-C30E', 'Steel-C30E', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-34CrNiMo6', 'Steel-34CrNiMo6', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-1C60', 'Steel-1C60', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S380MC', 'Steel-S380MC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Glass-Generic', 'Glass-Generic', 'Poisson ratio: 0.22, Youngs modulus: 72000.0 MPa'),
                        ('Steel-E295-GC', 'Steel-E295-GC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-C15', 'Steel-C15', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-G20Mn5', 'Steel-G20Mn5', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-St-E-380', 'Steel-St-E-380', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S500MC', 'Steel-S500MC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-C60E', 'Steel-C60E', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S335JO', 'Steel-S335JO', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-E360-GC', 'Steel-E360-GC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-C25E', 'Steel-C25E', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-3C35', 'Steel-3C35', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Acrylic-Glass-Generic', 'Acrylic-Glass-Generic', 'Poisson ratio: 0.38, Youngs modulus: 2550.0 MPa'),
                        ('Steel-E360', 'Steel-E360', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJMW-450-7', 'Steel-EN-GJMW-450-7', 'Poisson ratio: 0.3, Youngs modulus: 175000.0 MPa'),
                        ('Steel-S235JO', 'Steel-S235JO', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('PTFE-Generic', 'PTFE-Generic', 'Poisson ratio: 0.46, Youngs modulus: 564.0 MPa'),
                        ('Steel-EN-GJL-150', 'Steel-EN-GJL-150', 'Poisson ratio: 0.3, Youngs modulus: 95000.0 MPa'),
                        ('Steel-X6CrNiTi18-10', 'Steel-X6CrNiTi18-10', 'Poisson ratio: 0.3, Youngs modulus: 200000.0 MPa'),
                        ('Steel-G260', 'Steel-G260', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-C50E', 'Steel-C50E', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJMB-650-2', 'Steel-EN-GJMB-650-2', 'Poisson ratio: 0.3, Youngs modulus: 175000.0 MPa'),
                        ('Steel-G300', 'Steel-G300', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJMB-550-4', 'Steel-EN-GJMB-550-4', 'Poisson ratio: 0.3, Youngs modulus: 175000.0 MPa'),
                        ('Steel-St-37-2K', 'Steel-St-37-2K', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('PVC-Generic', 'PVC-Generic', 'Poisson ratio: 0.38, Youngs modulus: 2800.0 MPa'),
                        ('Steel-EN-GJMW-360-12', 'Steel-EN-GJMW-360-12', 'Poisson ratio: 0.3, Youngs modulus: 175000.0 MPa'),
                        ('Wood-Generic', 'Wood-Generic', 'Poisson ratio: 0.05, Youngs modulus: 12000.0 MPa'),
                        ('Steel-St-E-460', 'Steel-St-E-460', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('PP-Generic', 'PP-Generic', 'Poisson ratio: 0.44, Youngs modulus: 1470.0 MPa'),
                        ('Steel-G30Mn5', 'Steel-G30Mn5', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJMW-400-5', 'Steel-EN-GJMW-400-5', 'Poisson ratio: 0.3, Youngs modulus: 175000.0 MPa'),
                        ('Steel-S275N', 'Steel-S275N', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJMW-350-4', 'Steel-EN-GJMW-350-4', 'Poisson ratio: 0.3, Youngs modulus: 175000.0 MPa'),
                        ('Steel-C10', 'Steel-C10', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJL-200', 'Steel-EN-GJL-200', 'Poisson ratio: 0.3, Youngs modulus: 105000.0 MPa'),
                        ('Steel-30CrNiMo8', 'Steel-30CrNiMo8', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJL-100', 'Steel-EN-GJL-100', 'Poisson ratio: 0.3, Youngs modulus: 88000.0 MPa'),
                        ('Steel-EN-GJL-350', 'Steel-EN-GJL-350', 'Poisson ratio: 0.3, Youngs modulus: 135000.0 MPa'),
                        ('AlMgSi1F31', 'AlMgSi1F31', 'Poisson ratio: 0.3, Youngs modulus: 70000.0 MPa'),
                        ('Concrete-Generic', 'Concrete-Generic', 'Poisson ratio: 0.17, Youngs modulus: 32000.0 MPa'),
                        ('Steel-S420N', 'Steel-S420N', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-3C15', 'Steel-3C15', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJMB-350-10', 'Steel-EN-GJMB-350-10', 'Poisson ratio: 0.3, Youngs modulus: 175000.0 MPa'),
                        ('Reinforcement-FIB-B500', 'Reinforcement-FIB-B500', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJS-800-1', 'Steel-EN-GJS-800-1', 'Poisson ratio: 0.3, Youngs modulus: 180000.0 MPa'),
                        ('Steel-S355J2G3', 'Steel-S355J2G3', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-G16Mn5', 'Steel-G16Mn5', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-G230', 'Steel-G230', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('AlZn4-5Mg1F35', 'AlZn4-5Mg1F35', 'Poisson ratio: 0.3, Youngs modulus: 70000.0 MPa'),
                        ('Steel-20NiCrMo2', 'Steel-20NiCrMo2', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-E295', 'Steel-E295', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S235JR', 'Steel-S235JR', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJS-500-7', 'Steel-EN-GJS-500-7', 'Poisson ratio: 0.3, Youngs modulus: 170000.0 MPa'),
                        ('PLA-Generic', 'PLA-Generic', 'Poisson ratio: 0.36, Youngs modulus: 3640.0 MPa'),
                        ('Steel-3V45', 'Steel-3V45', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Aluminum-6061-T6', 'Aluminum-6061-T6', 'Poisson ratio: 0.33, Youngs modulus: 69000.0 MPa'),
                        ('ABS-Generic', 'ABS-Generic', 'Poisson ratio: 0.37, Youngs modulus: 2300.0 MPa'),
                        ('Steel-17CrNiMo6', 'Steel-17CrNiMo6', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJS-400-15', 'Steel-EN-GJS-400-15', 'Poisson ratio: 0.3, Youngs modulus: 167000.0 MPa'),
                        ('Steel-St-E-315', 'Steel-St-E-315', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-E335', 'Steel-E335', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S185', 'Steel-S185', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-Generic', 'Steel-Generic', 'Poisson ratio: 0.3, Youngs modulus: 200000.0 MPa'),
                        ('Steel-S420MC', 'Steel-S420MC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S275JR', 'Steel-S275JR', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-X3CrNiMo13-14', 'Steel-X3CrNiMo13-14', 'Poisson ratio: 0.3, Youngs modulus: 216000.0 MPa'),
                        ('Steel-C40E', 'Steel-C40E', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-X5CrNiMo17-12-2', 'Steel-X5CrNiMo17-12-2', 'Poisson ratio: 0.3, Youngs modulus: 180000.0 MPa'),
                        ('Steel-C22E', 'Steel-C22E', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-E335-GC', 'Steel-E335-GC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S260NC', 'Steel-S260NC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S275JO', 'Steel-S275JO', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-1C22', 'Steel-1C22', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-C55E', 'Steel-C55E', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-36NiCrMo16', 'Steel-36NiCrMo16', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-36CrNiMo4', 'Steel-36CrNiMo4', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S335JR', 'Steel-S335JR', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('CalculiX-Steel', 'CalculiX-Steel', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJS-600-3', 'Steel-EN-GJS-600-3', 'Poisson ratio: 0.3, Youngs modulus: 177000.0 MPa'),
                        ('Steel-X2CrNiMoN17-13-3', 'Steel-X2CrNiMoN17-13-3', 'Poisson ratio: 0.3, Youngs modulus: 200000.0 MPa'),
                        ('Steel-S235JRG1', 'Steel-S235JRG1', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S460N', 'Steel-S460N', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S460MC', 'Steel-S460MC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-S550MC', 'Steel-S550MC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-15CrNi6', 'Steel-15CrNi6', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Concrete-EN-C35_45', 'Concrete-EN-C35_45', 'Poisson ratio: 0.17, Youngs modulus: 32000.0 MPa'),
                        ('Steel-St-E-255', 'Steel-St-E-255', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-EN-GJL-250', 'Steel-EN-GJL-250', 'Poisson ratio: 0.3, Youngs modulus: 115000.0 MPa'),
                        ('Steel-S340MC', 'Steel-S340MC', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-St-E-500', 'Steel-St-E-500', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-1C45', 'Steel-1C45', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-X5CrNi18-10', 'Steel-X5CrNi18-10', 'Poisson ratio: 0.3, Youngs modulus: 200000.0 MPa'),
                        ('AlMg3F24', 'AlMg3F24', 'Poisson ratio: 0.3, Youngs modulus: 70000.0 MPa'),
                        ('Steel-G200', 'Steel-G200', 'Poisson ratio: 0.3, Youngs modulus: 210000.0 MPa'),
                        ('Steel-X2CrNiN24-4', 'Steel-X2CrNiN24-4', 'Poisson ratio: 0.3, Youngs modulus: 200000.0 MPa'),
                        ('Steel-EN-GJS-700-2', 'Steel-EN-GJS-700-2', 'Poisson ratio: 0.3, Youngs modulus: 180000.0 MPa')],

                default='PLA-Generic',
                description="Material of the object")
