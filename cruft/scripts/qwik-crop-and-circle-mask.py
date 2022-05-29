import tifffile as tf
import numpy as np
import os
import time

# take single tiff stack, crop and mask with one big circle
# useful for like, a petri dish recording
# set crop
x1, y1, dx, dy = 200, 200, 3100, 3100

# load tiff
wd = 'C:/Users/rldun/Desktop/GFP/20190731_1percentAgar_100animals_starved_Neopixel2LED_top/'
fname = '20190731_1percentAgar_100animals_starved_Neopixel2LED_top.tif'
f = tf.TiffFile(wd + fname)

# set outut file
output_fname = wd + '20190731_1percentAgar_100animals_starved_Neopixel2LED_top_crop-circled.tiff'
tw = tf.TiffWriter(output_fname, bigtiff=True)

# build mask
a = int(dx/2)
b = int(dy/2)
n = dx
r = n/2
y, x = np.ogrid[-a:n-a, -b:n-b]
mask = x*x + y*y <= r*r
array = np.zeros((n, n), dtype=f.pages[0].asarray().dtype)
array[mask] = 1

t0 = time.time()
try: 
    for ndx, p in enumerate(f.pages):

        # grab frame
        frame = p.asarray()

        # apply crop
        crop = frame[y1:y1+dy, x1:x1+dx]

        # apply circle
        circled = crop * mask

        # save
        tw.save(np.expand_dims(np.expand_dims(circled, 0), 0))

        # display progress
        if ndx % 100 == 0:
            print('At frame {} of {}. We have been going for {} seconds.'.format(ndx, len(f.pages), time.time()-t0))

except Exception as err:

    print('Error encountered: {}'.format(err))

    # close tiffwriter
    tw.close()
    t1 = time.time()

finally:

    tw.close()
    t1 = time.time()

print('That took {} seconds'.format(t1 - t0))
