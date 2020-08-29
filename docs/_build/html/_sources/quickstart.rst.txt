Quickstart
==========

Initialize
----------

.. figure:: ./ini.png
    :figwidth: 32%
    :align: right

* Design space can be initialized via two modes.
* ``SHAPE`` defines existing geometry as design space.
* ``HULL`` forms a convexhull excluding existing objects.
* Design space is then saved as a ``.stl`` file under the specified ``workspace_path``

\

.. image:: ./initialize.gif
   :alt: Initialize

Define
------
.. figure:: ./def.png
    :figwidth: 32%
    :align: right

* Specify the ``number of forces`` acting on the object.
* Assign materials to face(s) corresponding to each force.
* Assign vertex groups to edges that depict the direction of each corresponding force.
* Input the magnitude and click the ``Expand`` button to visualize each one of the aaplied forces.

Generate
--------

Visualize
---------