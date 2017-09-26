import maya.api.OpenMaya as om


def run(name, *args, **kwargs):
    """Get an MObject from the specified name.

    :param str name: name of the object.
    :rtype: MObject
    """

    sel = om.MSelectionList()
    sel.add(name)
    return sel.getDependNode(0)
