"""
Helper function to take a directory of tiffs, crop, and 
reformat as hyperstack using tiffile.
Tries to do it streaming style.

"""
import tifffile as tf
import numpy as np
import os
import time


x1, y1, dx, dy = 87, 0, 300, 80
# wd = 'C:/Users/rldun/Desktop/FC053_PANNEURONAL_GCAMP6F_MK2ASH_030519/tiff_stacks/runA_8MIN_run1(0-100sec)/'
# wd = 'C:/Users/rldun/Desktop/FC053_PANNEURONAL_GCAMP6F_MK2ASH_030519/tiff_stacks/runA_8MIN_run1(100-300sec)/'
wd = 'C:/Users/rldun/Desktop/FC053_PANNEURONAL_GCAMP6F_MK2ASH_030519/tiff_stacks/runA_8MIN_run1(300-479sec)/'
# wd = 'C:/Users/rldun/Desktop/test_tiff_writing/'

# get files in dir
fnames = os.listdir(wd)

# initialize output
outfile = 'combined_cropped.tiff'
tw = tf.TiffWriter(wd + outfile, bigtiff=True)

# assumes ordered, sequential
total_writes = 0

# calculate total frames
try:
    total_frames = 0
    for f in fnames:
        tiff = tf.TiffFile(wd + f)
        total_frames += len(tiff.pages)
except Exception as err:
    print('Error during pre-check: {}'.format(err))
    print('Quitting...')
    exit()

# print a helpful output
print('Streaming {} frames from {} files.'.format(total_frames, len(fnames)))
frame_print_num = total_writes // 15
t0 = time.time()
# do processing
# iterate pages and crop
frame_holder = np.zeros((dy, dx), dtype=tiff.pages[0].asarray().dtype)
try:
    for f in fnames:
        tiff = tf.TiffFile(wd + f)

        for p in tiff.pages:
            frame = p.asarray()
            crop = frame[y1:y1+dy, x1:x1+dx]
            frame_holder[:, :] = crop

            # write
            tw.save(frame_holder)
            total_writes += 1

            # display when important...
            percent_done = 100 * (total_writes / total_frames)
            t = time.time()
            time_left = (t - t0) / (percent_done / 100) - (t - t0)
            if total_writes % frame_print_num == 0:
                print('%{:.2f} done, {} frames written. ~{:.2f}s left...'.format(percent_done, total_writes, time_left))

except Exception as err:
    print('Oh no! Something went wrong at frame {}: {}'.format(total_writes, err))

finally:

    # close and print
    tw.close()
    t1 = time.time()
    print('Done!')
    print('That took {} seconds.'.format(t1 - t0))


# for testing output
"""
import tifffile as tf

fname = 'C:/Users/rldun/Desktop/test_tiff_writing/combined_cropped.tiff'
fname = 'C:/Users/rldun/Desktop/FC053_PANNEURONAL_GCAMP6F_MK2ASH_030519/tiff_stacks/runA_8MIN_run1(0-100sec)/combined_cropped.tiff'
tiff = tf.TiffFile(fname)
"""