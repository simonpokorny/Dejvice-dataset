import os
import numpy as np
import open3d as o3d
import matplotlib
from pathlib import Path

class Dataset():
    def __init__(self, dir: Path):
        """
        :param dir: Path to dataset Dejvice
        """
        self.pcl = os.listdir(dir / "pcl")
        self.pcl.sort()
        self.gps = os.listdir(dir / "poses")
        self.gps.sort()
        self.dir = dir
        self.cmap = matplotlib.cm.get_cmap('Greys')

    def __getitem__(self, item):
        data = np.load(self.dir / "data" / self.pcl[item])
        pointcloud = data["pcl"]
        T = np.loadtxt(self.dir / "poses" / self.gps[item])
        return pointcloud, T

    def vis_frame(self, idx, frame: bool = False, vis=True):
        """
        :param idx: Index of frame to visualize
        :param frame: vis frame of current pose
        :param vis: ---
        :return:
        """
        try:
            pointcloud, T = self.__getitem__(idx)
        except:
            raise IndexError
        else:
            vis_objects = []
            xyz = pointcloud[:, :3]
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(xyz)
            vis_objects.append(pcd)

            if frame:
                frame_pcl = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1)
                frame_pcl.rotate(T[:3, :3], center=(0, 0, 0))
                trans = tuple(T[:3, 3].reshape(-1, 1))
                frame_pcl = frame_pcl.translate(trans, relative=False)
                vis_objects.append(frame_pcl)

            if vis: self.visualization(vis_objects)
            return vis_objects

    def vis_seq(self, range_idx: tuple = (0, 1), BW: bool = False, frame: bool = False):
        """
        :param range_idx: tuple of range - frames in range are visualized
        :param BW: vis in black and white mode
        :param frame: vis the frames of poses
        :return: None
        """

        if BW:
            color_idx = np.linspace(0, 1, range_idx[1] - range_idx[0])

        vis_objects = []
        for idx in range(range_idx[0], range_idx[1]):
            scene = self.vis_frame(idx, frame=frame, vis=False)
            if BW: scene[0].paint_uniform_color(list(self.cmap(color_idx[idx - range_idx[0]])[:3]))
            vis_objects += scene
        self.visualization(vis_objects)

    @classmethod
    def visualization(cls, objects: list):
        o3d.visualization.draw_geometries(objects)


if __name__ == "__main__":

    scr_dir = Path("data")
    dataset = Dataset(scr_dir)
    # dataset.vis_frame(10, frame=True)
    # dataset.vis_seq((10, 20), BW=True, frame=True)
