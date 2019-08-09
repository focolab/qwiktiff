# requirements
# pip install pims_nd2 tifffile numpy
import tifffile as tf
import numpy as np
from pims import ND2_Reader
import time


# user parameters
fname = 'C:/Users/rldun/Desktop/temp rld test/test_080819.nd2'
num_z = 10

# begin code
if not fname.endswith('.nd2'):
    print('Filename should end with .nd2 !!! Exiting...')
    exit()

print('Converting ND2 file to tiff!')

# load nd2 file
frames = ND2_Reader(fname)

# check if nd2 file already has z planes specified
sizes = frames.sizes
if 'z' in sizes:
    print('Dataset is already organized with z = {}'.format(sizes['z']))
    if sizes['z'] != num_z:
        print('Dataset z does not match input z! Exiting :(')
        exit()

# guess at number of 2gb files we want to output
if frames.pixel_type != np.uint16:
    print('Pixel data type not recognized! Currently only supports uint16')

# xyz * 16 bit / 8 bits per byte
volume_byte_size = sizes['x'] * sizes['y'] * num_z * 16 / 8

# 2 billion bytes is 2gb
vols_per_file = int(np.floor(2000000000 / volume_byte_size))
if 'z' in sizes:
    total_files_to_output = int(np.ceil(sizes['t']/vols_per_file))
else:
    total_files_to_output = int(np.ceil(sizes[t] * num_z / vols_per_file))

# set total number of volumes to write
if 'z' not in sizes:
    if sizes['t'] % num_z != 0:
        print('Number of frames {} is not evenly divisible by {}. Clipping last frames...'.format(sizes['t'], num_z))
    vols_to_write = sizes['t'] // num_z

else:
    vols_to_write = sizes['t']

# start writing volumes to tiff file
output_fname_base = fname[:-4] + '_converted_'
vol_counter = 0
file_counter = 0
t0 = time.time()
try:
    for output_ndx in range(total_files_to_output):

        # set output fname with padded zeros
        tw = tf.TiffWriter(output_fname_base + str(file_counter).zfill(4) + '.tiff', bigtiff=True)

        # assemble and write volumes
        for v in range(vols_per_file):

            # helpful print statement on progress
            if vol_counter % 100 == 0:
                print('Writing volume {} of {}'.format(vol_counter, vols_to_write))
            
            # assemble a volume from individual frames
            if 'z' not in sizes:
                vol = zeros(num_z, sizes['y'], sizes['x'])
                for f in range(num_z):
                    frame_ndx = vol_counter * num_z + f
                    vol[f, :, :] = frames[frame_ndx]

            # otherwise we're already separated into volumes
            else:
                vol = frames[vol_counter]

            # write as zcyx (so final is tzcyx)
            tw.save(vol.reshape((num_z, 1, sizes['y'], sizes['x'])))

            # incrememnt volume counter for next loop
            vol_counter = vol_counter + 1

            # if we've reached the correct number of volumes, quit!
            if vol_counter == vols_to_write:
                raise('Done!')

        # close that tiff writer
        tw.close()

        # incrememnt file counter
        file_counter = file_counter + 1

# handle any errors or output
except Exception as err:
    print(err)
    frames.close()
    tw.close()

# clean up when we're done...
finally:
    print('That all took {} seconds!'.format(time.time() - t0))
    tw.close()
    frames.close()
    print('Done! Hope we did not have any errors... If you saw "exceptions must derive from BaseException" that doesnt matter...')

# close nd2
frames.close()
