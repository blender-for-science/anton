import bpy
import os
import subprocess
import numpy as np

class Anton_OT_Processor(bpy.types.Operator):
    bl_idname = 'anton.process'
    bl_label = 'Anton_Processor'
    bl_description = 'Start Optimization'

    material_library = {'Steel-28Mn6': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S690MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'PA6-Generic': {'POISSON': 0.39, 'YOUNGS': 2930.0},
                        'Steel-X39CrMo17-1': {'POISSON': 0.3, 'YOUNGS': 213000.0},
                        'Steel-S335N': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-3C22': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'PET-Generic': {'POISSON': 0.36, 'YOUNGS': 3150.0},
                        'Steel-1C35': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-2C10': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJL-300': {'POISSON': 0.3, 'YOUNGS': 125000.0},
                        'Steel-C30E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-34CrNiMo6': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-1C60': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S380MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Glass-Generic': {'POISSON': 0.22, 'YOUNGS': 72000.0},
                        'Steel-E295-GC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-C15': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-G20Mn5': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-St-E-380': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S500MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-C60E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S335JO': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-E360-GC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-C25E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-3C35': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Acrylic-Glass-Generic': {'POISSON': 0.38, 'YOUNGS': 2550.0},
                        'Steel-E360': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMW-450-7': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Steel-S235JO': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'PTFE-Generic': {'POISSON': 0.46, 'YOUNGS': 564.0},
                        'Steel-EN-GJL-150': {'POISSON': 0.3, 'YOUNGS': 95000.0},
                        'Steel-X6CrNiTi18-10': {'POISSON': 0.3, 'YOUNGS': 200000.0},
                        'Steel-G260': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-C50E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMB-650-2': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Steel-G300': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMB-550-4': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Steel-St-37-2K': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'PVC-Generic': {'POISSON': 0.38, 'YOUNGS': 2800.0},
                        'Steel-EN-GJMW-360-12': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Wood-Generic': {'POISSON': 0.05, 'YOUNGS': 12000.0},
                        'Steel-St-E-460': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'PP-Generic': {'POISSON': 0.44, 'YOUNGS': 1470.0},
                        'Steel-G30Mn5': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMW-400-5': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Steel-S275N': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMW-350-4': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Steel-C10': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJL-200': {'POISSON': 0.3, 'YOUNGS': 105000.0},
                        'Steel-30CrNiMo8': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJL-100': {'POISSON': 0.3, 'YOUNGS': 88000.0},
                        'Steel-EN-GJL-350': {'POISSON': 0.3, 'YOUNGS': 135000.0},
                        'AlMgSi1F31': {'POISSON': 0.3, 'YOUNGS': 70000.0},
                        'Concrete-Generic': {'POISSON': 0.17, 'YOUNGS': 32000.0},
                        'Steel-S420N': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-3C15': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJMB-350-10': {'POISSON': 0.3, 'YOUNGS': 175000.0},
                        'Reinforcement-FIB-B500': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJS-800-1': {'POISSON': 0.3, 'YOUNGS': 180000.0},
                        'Steel-S355J2G3': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-G16Mn5': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-G230': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'AlZn4-5Mg1F35': {'POISSON': 0.3, 'YOUNGS': 70000.0},
                        'Steel-20NiCrMo2': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-E295': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S235JR': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJS-500-7': {'POISSON': 0.3, 'YOUNGS': 170000.0},
                        'PLA-Generic': {'POISSON': 0.36, 'YOUNGS': 3640.0},
                        'Steel-3V45': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Aluminum-6061-T6': {'POISSON': 0.33, 'YOUNGS': 69000.0},
                        'ABS-Generic': {'POISSON': 0.37, 'YOUNGS': 2300.0},
                        'Steel-17CrNiMo6': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJS-400-15': {'POISSON': 0.3, 'YOUNGS': 167000.0},
                        'Steel-St-E-315': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-E335': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S185': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-Generic': {'POISSON': 0.3, 'YOUNGS': 200000.0},
                        'Steel-S420MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S275JR': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-X3CrNiMo13-14': {'POISSON': 0.3, 'YOUNGS': 216000.0},
                        'Steel-C40E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-X5CrNiMo17-12-2': {'POISSON': 0.3, 'YOUNGS': 180000.0},
                        'Steel-C22E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-E335-GC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S260NC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S275JO': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-1C22': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-C55E': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-36NiCrMo16': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-36CrNiMo4': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S335JR': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'CalculiX-Steel': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJS-600-3': {'POISSON': 0.3, 'YOUNGS': 177000.0},
                        'Steel-X2CrNiMoN17-13-3': {'POISSON': 0.3, 'YOUNGS': 200000.0},
                        'Steel-S235JRG1': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S460N': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S460MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-S550MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-15CrNi6': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Concrete-EN-C35_45': {'POISSON': 0.17, 'YOUNGS': 32000.0},
                        'Steel-St-E-255': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-EN-GJL-250': {'POISSON': 0.3, 'YOUNGS': 115000.0},
                        'Steel-S340MC': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-St-E-500': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-1C45': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-X5CrNi18-10': {'POISSON': 0.3, 'YOUNGS': 200000.0},
                        'AlMg3F24': {'POISSON': 0.3, 'YOUNGS': 70000.0},
                        'Steel-G200': {'POISSON': 0.3, 'YOUNGS': 210000.0},
                        'Steel-X2CrNiN24-4': {'POISSON': 0.3, 'YOUNGS': 200000.0},
                        'Steel-EN-GJS-700-2': {'POISSON': 0.3, 'YOUNGS': 180000.0}}

    def execute(self, context):
        """Solves the optimization problem defined by ``nodes``, ``elements``, ``fixed``, ``non_design_nodes``, ``youngs``, ``poisson``.
        Loads the saved numpy variables and computes stiffness matrix with a pyOptFEM vectorized function,
        solves for displacement and heads on to the optimization loop.

        :ivar convergence: Convergence of sensitivity for optimization
        :vartype convergence: ``float``

        :ivar fixed_elements: Indices of fixed elements
        :vartype fixed_elements: *numpy.array* of ``int``
        :ivar forced_elements: Indices of forced elements
        :vartype forced_elements: *numpy.array* of ``int``
        :ivar non_design_set: Non-design space elements
        :vartype non_design_set: *numpy.array* of ``int``

        :ivar edofmat: Element DOF mapping
        :vartype edofmat: *numpy.array* of ``int``

        :ivar free: Indices of free nodes
        :vartype free: *numpy.array* of ``int``
        :ivar element_centers: Centroid of each element
        :vartype element_centers: *numpy.array* of ``float``
        :ivar structure: Neighbourhood of an element
        :vartype structure: *numpy.array* of ``int``
        :ivar distances: Distance to each neighbour
        :vartype distances: *numpy.array* of ``float``
        :ivar volumes: Volume of each element
        :vartype volumes: *numpy.array* of ``float``

        :ivar K: Global stiffness matrix
        :vartype K: *numpy.array* of ``float``
        :ivar F: Force vector
        :vartype F: *numpy.array* of ``float``
        :ivar displacement: Displacement vector
        :vartype displacement: *numpy.array* of ``float``
        :ivar Ue: Element displacement vector
        :vartype Ue: *numpy.array* of ``float``

        :ivar densities: Density of each element
        :vartype densities: *numpy.array* of ``float``
        :ivar sensitivity: Sensitivity of each element
        :vartype sensitivity: *numpy.array* of ``float``

        :ivar fdensities: Filtered density vector
        :vartype fdensities: *numpy.array* of ``float``
        :ivar fsensitivity: Filtered sensitivity vector
        :vartype fsensitivity: *numpy.array* of ``float``

        :return: ``FINISHED`` if successful, ``CANCELLED`` otherwise

        \\
        """

        scene = context.scene
        if scene.anton.defined:
            subprocess.call(["python3", "./optimizer.py",
                                scene.anton.workspace_path,
                                scene.anton.filename,
                                "{}".format(scene.anton.number_of_iterations),
                                "{}".format(scene.anton.res),
                                "{}".format(scene.anton.volumina_ratio),
                                "{}".format(scene.anton.penalty_exponent),
                                "{}".format(scene.anton.include_forced),
                                "{}".format(scene.anton.include_fixed),
                                "{}".format(scene.anton.nds_density),
                                "{}".format(self.material_library[scene.anton.material]['YOUNGS']),
                                "{}".format(self.material_library[scene.anton.material]['POISSON'])])
            return {'FINISHED'}

        else:
            self.report({'ERROR'}, '.inp file missing in {}'.format(scene.anton.workspace_path))
            return {'CANCELLED'}
