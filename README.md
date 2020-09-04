# anton
[![Blender](https://img.shields.io/badge/Blender-2.80%2B-orange)](https://www.blender.org/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e0da62cdb7bc499b95bf70c18e8013cd)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=blender-for-science/anton&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/anton/badge/?version=latest)](https://anton.readthedocs.io/en/latest/?badge=latest)
[![Release](https://img.shields.io/github/v/release/blender-for-science/anton)](https://github.com/blender-for-science/anton/releases)
[![License](https://img.shields.io/github/license/blender-for-science/blendmsh)](https://github.com/blender-for-science/anton/blob/master/LICENSE.md)
[![Discord](https://img.shields.io/discord/750488363571740747?color=738ADB&label=Discord&style=flat-square)](https://discord.gg/tpq7Yuv)

![anton](./anton.gif)

``anton`` is an open-source generative design framework built on Blender, the open-source 3D creation suite. At its current stage of development, anton uses a density-based topology optimization methodology as a design generator and uses implicit surfaces for mesh generation.

## Installation
* Download the latest release
* Open Blender and head over to ``Edit`` -> ``Preferences`` -> ``Add-ons`` -> ``Install``
* Navigate to the downloaded **.zip** file and click ``Install Add-on``
* Enable the installed add-on, anton looks for the these python modules,
    * ``Numpy``
    * ``Scipy``
    * ``Scikit-learn``
    * ``gmsh-api``
    * ``tqdm``
* If you dont have these modules installed, click ``Install required modules``

## Documentation
Read more about anton: https://anton.readthedocs.io/en/latest/
