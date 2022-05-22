import copy

import numpy as np
import os
import open3d as o3d

from dataset import Dataset
from HD_maps import HD_map
from pathlib import Path


class Annotator(Dataset):
    def __init__(self, dir: Path):
        super().__init__(dir)
        self.HD_maps = HD_map()
        self.preprocessing_done = False

        # colors RGB for each class
        self.color_road = np.array([0, 0, 255])  # blue
        self.color_crosswalk = np.array([219, 48, 130])  # pink
        self.color_greenery = np.array([155, 239, 5])  # green

        # label for each class
        self.label_undefined = 0
        self.label_road = 1
        self.label_crosswalk = 2
        self.label_greenery = 3

        self.label_dict = {"road": 1, "crosswalk": 2, "greenery": 3}

    def __getitem__(self, item):
        data = np.load(self.dir / "pcl" / self.pcl[item])
        pointcloud = data["pcl"]
        T = np.loadtxt(self.dir / "poses" / self.gps[item])

        if self.preprocessing_done:
            data = np.load(self.dir / "colors" / self.pcl[item])
            colors = data["colors"]

            data = np.load(self.dir / "label" / self.pcl[item])
            label = data["label"]
            return pointcloud, label, colors, T
        else:
            return pointcloud, self.pcl[item]

    def preprocessing(self):

        if (not os.path.exists(self.dir / "colors")) or (not os.path.exists(self.dir / "label")):
            print("Start preprocessing".center(30, "-"))
            os.mkdir(self.dir / "colors")
            os.mkdir(self.dir / "label")

            for idx, (pointcloud, file_idx) in enumerate(self):
                print(f"{file_idx}")

                colors = np.zeros((pointcloud.shape[0], 3))
                label = np.zeros(pointcloud.shape[0])

                # road label
                road_bool = self.HD_maps.in_road(pointcloud)
                label = np.where(road_bool, self.label_road, label)
                road_bool = np.repeat(road_bool.reshape((-1, 1)), 3, axis=1)
                colors = np.where(road_bool, self.color_road, colors)

                # crosswalk label
                crosswalk_bool = self.HD_maps.in_crosswalk(pointcloud)
                label = np.where(crosswalk_bool, self.label_crosswalk, label)
                crosswalk_bool = np.repeat(crosswalk_bool.reshape((-1, 1)), 3, axis=1)
                colors = np.where(crosswalk_bool, self.color_crosswalk, colors)

                # greenery label
                greenery_bool = self.HD_maps.in_greenery(pointcloud)
                label = np.where(greenery_bool, self.label_greenery, label)
                greenery_bool = np.repeat(greenery_bool.reshape((-1, 1)), 3, axis=1)
                colors = np.where(greenery_bool, self.color_greenery, colors)

                np.savez(self.dir / "colors" / file_idx, colors=colors)
                np.savez(self.dir / "label" / file_idx, label=label)
            print("End preprocessing".center(30, "-"))
        else:
            print("Preprocessing was already done".center(30, "-"))
        self.preprocessing_done = True

    def vis_frame(self, idx, cfg, frame=False, vis=True):
        """
        :param idx:
        :param cfg:
        :param frame:
        :param vis:
        :return:
        """
        try:
            pointcloud, label, colors, T = self.__getitem__(idx)
        except:
            raise IndexError
        else:

            pointcloud, colors = self._process_pcl(pointcloud, colors, label, T, cfg)
            vis_objects = []
            xyz = pointcloud[:, :3]
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(xyz)
            pcd.colors = o3d.utility.Vector3dVector(colors / 255)
            vis_objects.append(pcd)

            if frame:
                frame_pcl = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1)
                frame_pcl.rotate(T[:3, :3], center=(0, 0, 0))
                trans = tuple(T[:3, 3].reshape(-1, 1))
                frame_pcl = frame_pcl.translate(trans, relative=False)
                vis_objects.append(frame_pcl)

            if vis: self.visualization(vis_objects)
            return vis_objects

    def _process_pcl(self, pointcloud, colors, label, T, cfg):

        if cfg["specific_class"] in self.label_dict and "specific_class" in cfg:
            specific_class = self.label_dict[cfg["specific_class"]]
            mask = (label == specific_class)
            pointcloud = pointcloud[mask]
            colors = colors[mask]

        if "height_from_ego" in cfg:
            mask = (pointcloud[:, 2] - T[2,3]) > cfg["height_from_ego"]
            pointcloud = pointcloud[mask]
            colors = colors[mask]

        if "radius" in cfg:
            trans = T[:2, 3]
            xy = copy.deepcopy(pointcloud[:, :2]) - trans
            mask = ((xy[:, 0] ** 2 + xy[:, 1] ** 2) < (cfg["radius"] ** 2)) * ((xy[:, 0] ** 2 + xy[:, 1] ** 2) > (2 ** 2))
            pointcloud = pointcloud[mask]
            colors = colors[mask]

        return pointcloud, colors


if __name__ == "__main__":
    scr_dir = Path("../data")
    annotator = Annotator(dir=scr_dir)
    annotator.preprocessing()

    cfg_file = {"specific_class": "all",
                "height_from_ego": -3,
                # -1.55
                "radius": 20}

    annotator.vis_frame(idx=15, cfg=cfg_file)
