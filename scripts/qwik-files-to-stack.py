import tifffile as tf
import numpy as np
import os
import time

#wd = 'G:/GFP/20190723_GFP/20190723_1%agar_ir_200animals_diffused_walkingtest2/'
wd = 'G:/GFP/20190722_GFP_1_short/'

output_fname = wd + 'combined.tif'

# change working directory
os.chdir(wd)
file_list = os.listdir()

# output
tw = tf.TiffWriter(output_fname, bigtiff=True)

# temp test for hyperstack writing
# tlist = []

try:

    # load tiffs and append to output
    t0 = time.time()
    for ndx, fname in enumerate(file_list):
        tiff = tf.TiffFile(wd + fname).asarray()

        # add singleton dimensions and save
        # singletons arrange (xy)czt appropriately... this writes T
        tw.save(np.expand_dims(np.expand_dims(tiff, 0), 0))

        # example for writing one volume at a time
        # tlist.append(tiff)
        # if len(tlist) == 10:
            # to_write = np.array(tlist).reshape((10, 1, 3446, 3500))
            # tw.save(to_write)
            # tlist = []

        # print update
        if ndx % 100 == 0:
            print('At file: {}'.format(ndx))
            tn = time.time()
            print('We have been running for {} seconds.'.format(tn - t0))

except Exception as err:

    print('Error encountered: {}'.format(err))

    # close tiffwriter
    tw.close()
    t1 = time.time()

finally:

    tw.close()
    t1 = time.time()

print('That took {} seconds'.format(t1 - t0))

#########################

import h5py
import tifffile as tf

#numt = 4800
#numz = 1
#numx = 3500
#numy = 3446
#numc = 1

# load
fname = tf.TiffFile('20190723_1p_agar_ir_200animals_diffused_walkingtest2')
# fname = 'combined.tif'
arr = tf.TiffFile(fname + '.tif').asarray()

# save as h5
f = h5py.File(fname + '.h5', "w")
f.create_dataset('data', data=arr)
f.close()