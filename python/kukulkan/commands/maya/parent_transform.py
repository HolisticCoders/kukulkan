import maya.api.OpenMaya as om

import get_mobject


def run(child, parent=None, *args, **kwargs):
    """Parent an object to another

    :param child: MObject of the child node.
    :type child: MObject or str
    :param parent: MObject of the parent node.
    :type parent: MObject or str or None
    """
    dag_mod = om.MDagModifier()

    if parent is None:
        parent = om.MObject.kNullObj
    elif isinstance(parent, str):
        parent = get_mobject.run(parent)

    if isinstance(child, str):
        child = get_mobject.run(child)

    dag_mod.reparentNode(child, newParent=parent)
    dag_mod.doIt()
