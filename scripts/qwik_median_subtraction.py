import PIL.Image
import numpy as np

from tkinter import filedialog
from tkinter import *

import os

###############################
#uploading median tiff
#needs median tiff to already have been saved from Fiji


#directory where median image is
median_im = PIL.Image.open(os.path.expanduser('~/Desktop/Median_Tiffs/MED_20190807_2.tif'))
median_array = np.array(median_im)
median_array_16 = median_array.astype(np.int16)

###############################
#uploading each tiff, subtracting median from it, then exporting
num_frames = 4800

for x in range(1,num_frames+1):
    #directory where .tiff stack is (assumes) .tiffs are serialized with 6 digits
    im = PIL.Image.open(os.path.expanduser(r'/Volumes/TOSHIBA EXT/KatoLab_Recordings/20190807/20190807_1%agar_ir_blinkingLED_top_walkingtest2/'  + f'{x:06}.tiff'))

    imarray = np.array(im)
    imarray_16 = imarray.astype(np.int16)


    #subtraction of median
    np_subtr_16 = np.subtract(median_array_16, imarray_16)

    np_subtr_16 = np.absolute(np_subtr_16)
    np_subtr = np_subtr_16.astype(np.uint8)


    finalIm = PIL.Image.fromarray(np_subtr)
    #directory where output is saved
    finalIm.save(os.path.expanduser('~/Desktop/20190807_2_outputs/out' + f'{x:06}.tiff'))