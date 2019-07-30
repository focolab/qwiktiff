import h5py
import tifffile as tf
import time


# load
t0 = time.time()
fname = '20190723_1p_agar_ir_200animals_diffused_walkingtest2'
# fname = 'combined.tif'
arr = tf.TiffFile(fname + '.tif').asarray()
t1 = time.time()

print('Loading file took {} seconds.'.format(t1-t0))

# save as h5
f = h5py.File(fname + '.h5', "w")
f.create_dataset('data', data=arr)
f.close()
t2 = time.time()

print('Saving file took {} seconds. Together that took {} seconds.'.format(t2-t1, t2-t0))