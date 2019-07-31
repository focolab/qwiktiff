import tifffile as tf
import numpy as np
import os
import time

fnames = [
    '20190702_worma_488_1562085649114.tif',
    '20190702_wormb_488_wblive_1562086740921.tif',
    '20190702_wormc_561_1562088180319.tif',
    '20190702_wormd_561_1562089853661.tif'
]

# params for ordering
numz = 11

# batch processing
t0 = time.time()
for fname in fnames:

    t = time.time()

    # get filename
    fileroot, ext = os.path.splitext(fname)
    output_fname = fileroot + '_uint16.tif'

    # file i/o 
    fi = time.time()
    arr = tf.TiffFile(fname).asarray().astype(np.uint16)
    print('File {} took {} seconds to load.'.format(fname, time.time()-fi))
    tw = tf.TiffWriter(output_fname, imagej=True)

    # get dims... might already be formatted tzyx or tzcyx
    numt = arr.shape[0]
    numy = arr.shape[-2]
    numx = arr.shape[-1]

    # write TZCYX
    fo = time.time()
    tw.save(arr.reshape((numt, numz, 1, numy, numx)))
    tw.close()
    print('File {} took {} seconds to save'.format(output_fname, time.time() - fo))
    print('File {} took {} seconds to process end-to-end.'.format(fname, time.time() - t))

t1 = time.time()
print('All in all that took {} seconds.'.format(t1 - t0))