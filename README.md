# Dataset Dejvice

Motivation for collecting the dataset was an idea to automate a labeling process. We captured Dejvice's roundabout area in different time. This allow us to create a HD map and split points into static and dynamic subset. Based on this division and localization in HD maps we can create the bounding boxes around the points and statistically decide about a class. 

![giff](/data/gif/dataset.gif)

## Setup 

For collecting the data was used Oyster lidar and gps (todo name)
```
Oyster lidar
- 10 Hz
- 128 lines and 45° field of view vertically

GPS
- todo specs
```

## Calibration

TODO


## Description of the data

We captured 26563 frames, but only 18856 was available with accurate GPS. Dataset capture was divide into 9 sequnces. 
Visualization of sequences in Google map is available on [map link](https://www.google.com/maps/d/u/0/edit?mid=1KdB8-CveT3HbCh3U-pd8nBCAsRsPD6VV&usp=sharing).

### Overview

| seq_number | total frames | frames with accurate gps | color in map |
| ----- | ---- | ---- | ---- |
| seq_1 | 2178 | 1906 | ![#A52714](https://via.placeholder.com/15/A52714/000000?text=+) |
| seq_2 | 1866 | 1119 | ![#006064](https://via.placeholder.com/15/006064/000000?text=+) |
| seq_3 | 1905 | 1402 | ![#E65100](https://via.placeholder.com/15/E65100/000000?text=+) |
| seq_4 | 1946 | 1809 | ![#01579B](https://via.placeholder.com/15/01579B/000000?text=+) |
| seq_5 | 4762 | 3741 | ![#F9A825](https://via.placeholder.com/15/F9A825/000000?text=+) |
| seq_6 | 3983 |    0 | - |
| seq_7 | 7180 | 4011 | ![#817717](https://via.placeholder.com/15/817717/000000?text=+) |
| seq_8 | 5570 | 3762 | ![#558B2F](https://via.placeholder.com/15/558B2F/000000?text=+) |
| seq_9 | 1156 | 1106 | ![#097138](https://via.placeholder.com/15/097138/000000?text=+) |

### Google maps visualization

<img width="615" alt="map" src="https://user-images.githubusercontent.com/24698875/167591505-697f1747-d413-4c22-882e-65cd77a14079.png">



### Dataset structure

```
 data/
    pcl/
        01000001.npz
        01000002.npz
        01000003.npz
        ...
    poses/
        01000001.txt
        01000002.txt
        01000003.txt
        ...
    maps/
        gpx_files/
            seq1.gpx
            ...
            seq9.gpx
  -README.md

```

### Additional data

For 5 sequences was also captured mp4 video of front view.
```
-todo
```

### Online Repository link

On github are published only 10 frames from first sequence. Link for downloading all dataset -> link todo


## License

??? je potreba - 
templete:
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details








