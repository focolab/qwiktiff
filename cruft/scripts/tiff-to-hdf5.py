import h5py
import tifffile as tf
import time


# load
t0 = time.time()
#fname = '20190731_1percentAgar_100animals_starved_Neopixel2LED_top'
#fname='20190731_1percentAgar_100animals_starved_Neopixel2LED_top_crop-circled'
#fname = ''
fname = 'combined'

# fname = 'combined.tif'
arr = tf.TiffFile(fname + '.tiff').asarray()
t1 = time.time()

print('Loading file took {} seconds.'.format(t1-t0))

# save as h5
f = h5py.File(fname + '0-2400-2.h5', "w")
f.create_dataset('data', data=arr[:2400:2,:,:], compression="gzip")
f.close()
t2 = time.time()

print('Saving file took {} seconds. Together that took {} seconds.'.format(t2-t1, t2-t0))