import numpy as np
from haversine import haversine, Unit

"""
REF_POINT:
https://www.google.com/maps/place/50°06'02.1%22N+14°23'43.5%22E/@50.100595,14.3948798,157m/data=!3m2!1e3!4b1!4m6!3m5!1s0x0:0x295938f6e0bcf483!7e2!8m2!3d50.1005945!4d14.3954275!5m1!1e4

HELPER:
https://www.google.com/maps/place/50°06'02.1%22N+14°23'30.5%22E/@50.1005833,14.3896169,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0xc6e04cdac4f7b6d3!8m2!3d50.1005833!4d14.3918056

"""

REF_POINT = np.array([50.100595, 14.395427, 225.])  # (latitude, longitude, altitude)
HELPER = np.array([50.100595, 14.391806, 225.])  # (latitude, longitude, altitude)


def transformorm_point(coords: np.array([])):
    """
    Transformation of point from google maps area to coord system.
    :param coords: (2,)
    :param heading: float
    :return:
    """

    point_HELPER = (HELPER[0], HELPER[1])
    point_REF = (REF_POINT[0], REF_POINT[1])
    point_pcl = (coords[1], coords[0])  # HD maps are in (lon, lat), thus tf to (lat, lon)

    # input - (lat, lon)
    h = haversine(point_REF, point_pcl, unit=Unit.METERS)
    r = haversine(point_HELPER, point_pcl, unit=Unit.METERS)
    p = haversine(point_REF, point_HELPER, unit=Unit.METERS)

    # angle in clockwise direction
    if point_pcl[0] > 50.100595:  # higher in x-axis
        angle = np.arccos((p ** 2 + h ** 2 - r ** 2) / (2 * h * p))
        angle -= np.pi / 2
    else:
        angle = np.arccos((p ** 2 + h ** 2 - r ** 2) / (2 * h * p))
        angle = (np.pi - angle) + np.pi / 2

    x = h * np.sin(angle)
    y = h * np.cos(angle)
    t = np.array([x, y])

    return t
