"""
Helper function to take a linear or hyperstack tiff and save as individual z planes...

"""

import tifffile as tf

fname = '20190702_worma_488_1562085649114.tif'
#numz = 11

tiff = tf.TiffFile(fname).asarray()

# iterate zs and save
for z in range(tiff.shape[1]):
	tf.imwrite(fname + '_z' + str(z) + '.tif', tiff[:, z, :, :])