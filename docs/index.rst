.. anton documentation master file, created by
   sphinx-quickstart on Thu Aug 27 18:35:15 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to anton's documentation!
=================================

.. image:: https://img.shields.io/badge/Blender-2.80%2B-orange
   :target: https://www.blender.org/
   :alt: Blender

.. image:: https://app.codacy.com/project/badge/Grade/e0da62cdb7bc499b95bf70c18e8013cd
   :target: https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=blender-for-science/anton&amp;utm_campaign=Badge_Grade
   :alt: Codacy

.. image:: https://img.shields.io/github/license/blender-for-science/blendmsh
   :target: https://github.com/blender-for-science/anton/blob/master/LICENSE.md
   :alt: License

.. image:: https://badges.gitter.im/blender-for-science/community.svg
   :target: https://gitter.im/blender-for-science/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
   :alt: Gitter

.. image:: ../anton.gif
   :alt: anton


What is Generative design?
--------------------------

Generative design is a design exploration process that yields feasible design outcomes based on a set of well-defined 
constraints and performance objectives, using one or more optimization methodologies. In practice, Topology optimization is used to generate
numerous design outcomes by varying its parameters within an interval and the generated outcomes that best meet the performance objectives are filtered and processed further.

What is anton?
--------------

``anton`` is an open-source generative design framework built on Blender, the open-source 3D creation suite. 
At its current stage of development, anton uses a density-based topology optimization methodology as a design generator and
uses implicit surfaces for mesh generation.

.. toctree::
   :hidden:
   :maxdepth: 2

   installation
   quickstart
   scripts
   release
   license


