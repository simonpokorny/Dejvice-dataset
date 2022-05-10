import gpxpy
import gpxpy.gpx
import os
import numpy as np
from pathlib import Path

class GPS_dataset():
    def __init__(self, filename: str, src_dir: Path(), dst_dir: Path() = Path()):
        self.src_dir = src_dir
        self.files = os.listdir(src_dir)
        self.files.sort()
        self.dst_dir = dst_dir
        self.filename = filename

    def create_gpx(self):
        latitude, longitude, altitude = np.array([]), np.array([]), np.array([])

        for gps in self.files:
            gps_data = np.load(self.src_dir / gps)
            latitude = np.append(latitude, float(gps_data["latitude"]))
            altitude = np.append(altitude, float(gps_data["altitude"]))
            longitude = np.append(longitude, float(gps_data["longitude"]))

        mask = (longitude != 0) * (altitude != 0)
        gps_data = tuple(zip(latitude[mask], longitude[mask], altitude[mask]))

        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        for idx, (lat, lon, alt) in enumerate(gps_data):
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=alt))

        print('Created GPX:', gpx.to_xml())
        with open(f"{self.filename}.gpx", "w") as f:
            f.write(gpx.to_xml())


if __name__ == "__main__":

    src_dir = Path("dataset/seq_9_gps/")
    gps = GPS_dataset("tmp", src_dir)
    gps.create_gpx()


