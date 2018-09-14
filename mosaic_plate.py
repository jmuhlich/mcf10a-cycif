import sys
import pathlib
import numpy as np
import skimage.io
from ashlar.reg import build_pyramid


input_dir = pathlib.Path(sys.argv[1])
output_file = pathlib.Path(sys.argv[2])

PAD_WELL = 0.15
PAD_FIELD = 0.05
N_CHANNELS = 36
N_ROWS = 3
N_COLUMNS = 7

well_size = int(1024 * 3 + 1024 * PAD_FIELD * 2)
plate_height = int(well_size * N_ROWS + well_size * PAD_WELL * N_ROWS - 1) + 1
plate_width = int(well_size * N_COLUMNS + well_size * PAD_WELL * N_COLUMNS - 1) + 1

img = np.zeros((N_CHANNELS, plate_height, plate_width), np.uint16)

for row_i, row in enumerate('CDE'):
    for col_i, col in enumerate(range(4, 11)):
        print(row, col)
        for field_i in range(9):
            f_x = field_i % 3
            f_y = field_i // 3
            x = int(well_size * (1 + PAD_WELL) * col_i + 1024 * (1 + PAD_FIELD) * f_x)
            y = int(well_size * (1 + PAD_WELL) * row_i + 1024 * (1 + PAD_FIELD) * f_y)
            field = skimage.io.imread(str(input_dir / f'{row}{col:02}-{field_i}.tif'))
            img[:, y:y+1024, x:x+1024] = field[:N_CHANNELS]

skimage.io.imsave(
    str(output_file), img,
    description='!!xml!!', software='Ashlar (Glencoe/Faas pyramid output)',
    bigtiff=True, tile=(1024, 1024), photometric='minisblack'
)
build_pyramid(str(output_file), N_CHANNELS, img.shape, img.dtype.type, 1024, True)
