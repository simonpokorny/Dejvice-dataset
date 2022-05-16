import numpy as np
import pandas as pd
import re
from pathlib import Path
from transformation import transformorm_point
import os
import matplotlib.pyplot as plt

def polygon_str2np(element: str):
    return np.array([float(numb) for numb in re.findall("\d+\.\d+", element)]).reshape((-1, 2))


def process_csv(filename: Path()):
    df = pd.read_csv(f'HD_maps_polygons_csv/{filename}.csv')
    df["polygon_numpy"] = " "
    df["polygon_numpy_calibrated"] = " "

    for idx, fe in enumerate(df["WKT"]):
        fe = polygon_str2np(fe)
        fe_calib = np.zeros_like(fe)
        df["polygon_numpy"][idx] = fe
        for idx_p, point in enumerate(fe):
            fe_calib[idx_p] = transformorm_point(coords=point)
        df["polygon_numpy_calibrated"][idx] = fe_calib
    #filename = Path(str(filename) + "_calibrated")
    df.to_csv(f"HD_maps_polygons_csv/{filename}.csv", index=False)


def main():
    files = os.listdir("HD_maps_polygons_csv")
    #files = ["HD_map-zelen_calibrated.csv"]
    for file in files:
        if file == ".DS_Store":
            continue
        print(file)
        filename = Path(file[:-4])
        process_csv(filename)


if __name__ == "__main__":
    main()
