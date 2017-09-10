import maya.api.OpenMaya as om


def run():
    curveFn = om.MFnNurbsCurve()

    points = [
        (0, 1),
        (-0.5, 0.866025),
        (-0.866025, 0.5),
        (-1, 0),
        (-0.866025, -0.5),
        (-0.5, -0.866025),
        (0, -1),
        (0.5, -0.866025),
        (0.866025, -0.5),
        (1, 0),
        (0.866025, 0.5),
        (0.5, 0.866025),
        (0, 1),
    ]

    curve = curveFn.createWithEditPoints(
        points,
        3,
        om.MFnNurbsCurve.kPeriodic,
        True,
        True,
        True,
    )

    return curve


if __name__ == '__main__':
    run()
