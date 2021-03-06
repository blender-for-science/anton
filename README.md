# anton
[![Blender](https://img.shields.io/badge/Blender-2.80%2B-orange)](https://www.blender.org/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e0da62cdb7bc499b95bf70c18e8013cd)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=blender-for-science/anton&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/anton/badge/?version=latest)](https://anton.readthedocs.io/en/latest/?badge=latest)
[![Release](https://img.shields.io/github/v/release/blender-for-science/anton)](https://github.com/blender-for-science/anton/releases)
[![License](https://img.shields.io/github/license/blender-for-science/blendmsh)](https://github.com/blender-for-science/anton/blob/master/LICENSE.md)
[![Discord](https://img.shields.io/discord/750488363571740747?color=738ADB&label=Discord&style=flat-square)](https://discord.gg/tpq7Yuv)

![anton](./GE.gif)

``anton`` is an open-source generative design framework built on Blender, the open-source 3D creation suite. At its current stage of development, anton uses a narrow-band topology optimization methodology as a design generator and uses implicit surfaces for mesh generation.

## Dependencies
* ``taichi-build`` requires [spgrid_topo_opt](https://github.com/imsenthur/spgrid_topo_opt), a Narrow-Band Topology Optimization framework developed by [Haixiang Liu (University of Wisconsin-Madison)](http://pages.cs.wisc.edu/~cslhxac/), [Yuanming Hu (MIT CSAIL)](http://taichi.graphics/me/), [Bo Zhu (Dartmouth College)](http://www.dartmouth.edu/~boolzhu/), [Wojciech Matusik (MIT CSAIL)](https://cdfg.csail.mit.edu/wojciech), [Eftychios Sifakis (University of Wisconsin-Madison)](http://pages.cs.wisc.edu/~sifakis/).
* The following python modules are also required:
    * ``Numpy``
    * ``Scipy``
    * ``Scikit-learn``
    * ``gmsh-api``

## Installation
* For a minimal installation, download a ``native-build`` release.
* For more advanced and reliable results, download a ``taichi-build`` release.
* Open Blender and head over to ``Edit`` -> ``Preferences`` -> ``Add-ons`` -> ``Install``
* Navigate to the downloaded **.zip** file and click ``Install Add-on``

## Documentation
Read more about anton: https://anton.readthedocs.io/en/latest/
