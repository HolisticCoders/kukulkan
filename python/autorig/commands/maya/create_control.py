import maya.api.OpenMaya as om


def run(points=None, degree=None, *args, **kwargs):
    """Create a control.

    :param points:list of points in 2D space (x, y).
    :type points: list(tuple(float, float))
    :param int degree: degree of the curve.

    :return: The curve created.
    :rtype: MObject
    """

    curveFn = om.MFnNurbsCurve()

    if not points:
        points = [
            (1, 1),
            (-1, 1),
            (-1, -1),
            (1, -1),
            (1, 1),
        ]
    else:
        if not points[0] == points[-1]:
            points.append(points[0])

    if not degree:
        degree = 1

    curve = curveFn.createWithEditPoints(
        points,
        degree,
        om.MFnNurbsCurve.kPeriodic,
        True,
        True,
        True,
    )

    return curve
