from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import pandas as pd
import numpy as np
from pathlib import Path


def parse_df2np(df):
    points_out = np.zeros((df.shape[0]), dtype=object)
    for idx, points in enumerate(df):
        points = points.replace('[', '')
        points = points.replace(']', '')
        points = points.replace('\n', '')
        points = np.fromstring(points, dtype=float, sep=' ').reshape((-1, 2))
        points_out[idx] = points
    return points_out


def inside_polygon(polygon: Polygon, point: Point):
    if polygon.contains(point):
        return 1
    else:
        return 0


def inside_map_class(type_class, point: Point):
    for polygon in type_class:
        if inside_polygon(polygon, point):
            return 1
    return 0


class HD_map():
    def __init__(self, csv_dir: Path = Path("../maps/HD_maps_csv/")):
        crosswalk = pd.read_csv(csv_dir / "HD_map_crosswalk.csv")
        self.crosswalk = parse_df2np(crosswalk["polygon_numpy_calibrated"])
        self.crosswalk = [(lambda points: Polygon(points))(points) for points in self.crosswalk]

        greenery = pd.read_csv(csv_dir / "HD_map_greenery.csv")
        self.greenery = parse_df2np(greenery["polygon_numpy_calibrated"])
        self.greenery = [(lambda points: Polygon(points))(points) for points in self.greenery]

        road = pd.concat(
            [pd.read_csv(csv_dir / "HD_map_main_road.csv"), pd.read_csv(csv_dir / "HD_map_side_streets.csv")],
            ignore_index=True)
        self.road = parse_df2np(road["polygon_numpy_calibrated"])
        self.road = [(lambda points: Polygon(points))(points) for points in self.road]

    def in_road(self, points: np.array):
        in_road_bool = np.zeros((points.shape[0]))
        for idx, point in enumerate(points):
            if inside_map_class(self.road, Point(point[:2])):
                in_road_bool[idx] = 1
        return in_road_bool

    def in_crosswalk(self, points: np.array):
        in_crosswalk_bool = np.zeros((points.shape[0]))
        for idx, point in enumerate(points):
            if inside_map_class(self.crosswalk, Point(point[:2])):
                in_crosswalk_bool[idx] = 1
        return in_crosswalk_bool

    def in_greenery(self, points: np.array):
        in_greenery_bool = np.zeros((points.shape[0]))
        for idx, point in enumerate(points):
            if inside_map_class(self.greenery, Point(point[:2])):
                in_greenery_bool[idx] = 1
        return in_greenery_bool


if __name__ == "__main__":
    map = HD_map()

    points = np.array([[0, 0, 0]])
    map.in_crosswalk(points)
    map.in_greenery(points)
