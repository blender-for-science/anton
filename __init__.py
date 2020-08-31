# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#################################################

# -------------------
# Blender for Science
# -------------------
# Add-on: anton
# Author: Senthur Raj (Github: imsenthur)
# Description:
# https://github.com/blender-for-science/anton

#################################################

bl_info = {
    "name" : "anton",
    "author" : "Senthur Raj",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 1, 0),
    "location" : "View3D",
    "warning" : "",
    "wiki_url" : "https://anton.readthedocs.io/en/latest/",
    "tracker_url" : "https://github.com/blender-for-science/anton/issues",
    "category" : "Mesh"
}

import bpy
from collections import OrderedDict
from .preferences import AntonInstaller, AntonPreferences
from .panel import Anton_PT_Panel
from .properties import AntonPropertyGroup, ForcePropertyGroup
from .initializer import Anton_OT_ForceUpdater, Anton_OT_Initializer
from .definer import Anton_OT_DirectionUpdater, Anton_OT_Definer
from .processor import Anton_OT_Processor
from .visualizer import Anton_OT_Visualizer

classes = [AntonPreferences, AntonInstaller, Anton_PT_Panel, Anton_OT_Processor,
            AntonPropertyGroup, ForcePropertyGroup, Anton_OT_ForceUpdater, Anton_OT_Visualizer,
            Anton_OT_Initializer, Anton_OT_DirectionUpdater, Anton_OT_Definer]

def register():
    """Registers Preferences, Installer, Panel, PropertyGroup, ForcePropertyGroup,
    ForceUpdater, Initializer, DirectionUpdater, Definer, Processor, and
    Visualizer classes and instantiates scene variables load, forced_magnitudes
    and forced_direction_signs that are used by Processor.
    """

    for _class in classes:
        bpy.utils.register_class(_class)

    bpy.types.Scene.load = OrderedDict()
    bpy.types.Scene.forced_magnitudes = OrderedDict()
    bpy.types.Scene.forced_direction_signs = OrderedDict()

    bpy.types.Scene.anton = bpy.props.PointerProperty(type=AntonPropertyGroup)
    bpy.types.Scene.forceprop = bpy.props.CollectionProperty(type=ForcePropertyGroup)

def unregister():
    """Unregisters Preferences, Installer, Panel, PropertyGroup, ForcePropertyGroup,
    ForceUpdater, Initializer, DirectionUpdater, Definer, Processor, and
    Visualizer classes and deletes all the scene variables used by Processor.
    """
    for _class in classes:
        bpy.utils.unregister_class(_class)

    del bpy.types.Scene.load
    del bpy.types.Scene.forced_magnitudes
    del bpy.types.Scene.forced_direction_signs