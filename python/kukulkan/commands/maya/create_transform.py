import maya.api.OpenMaya as om


def run(*args, **kwargs):
    """Create a transform."""
    return om.MFnTransform().create()
