import sys
import time
import numpy as np
import logging
import h5pyd
if __name__ == "__main__":
    from config import Config
else:
    from .config import Config

#
# Main
#
# Crete a three-dimensional dataset of random floats.
#
# Argument can be used to set the size of the cube
#
cfg = Config()

loglevel = logging.ERROR  # Use logging.DEBUG to see the http requests
logging.basicConfig(format='%(asctime)s %(message)s', level=loglevel)
cube_side = 64

if len(sys.argv) > 1:
    if sys.argv[1] in ("-h", "--help"):
        print("Usage: python writecube.py [cube_side]")
        sys.exit(-1)
    else:
        cube_side = int(sys.argv[1])

filename = "/home/" + cfg["hs_username"] + "/"
filename += "cube_" + str(cube_side) + ".h5"

print("creating domain:", filename)
f = h5pyd.File(filename, "a") 

print("filename,", f.filename)

print("create dataset")

if "dset" not in f:
    dset = f.create_dataset('dset', (cube_side, cube_side, cube_side), dtype='f8')
else:
    dset = f["dset"]

print("name:", dset.name)
print("shape:", dset.shape)
print("dset.type:", dset.dtype)
print("chunk layout:", dset.chunks)
chunk_size = np.prod(dset.chunks) * dset.dtype.itemsize
print("chunk size: {:.2f}m".format(chunk_size/(1024.0*1024.0)))
chunks_per_slice = (dset.shape[1] // dset.chunks[1])*(dset.shape[2] // dset.chunks[2])
print("chunks per slice: {}".format(chunks_per_slice))

print("writing data...")

for i in range(cube_side):
    print("writing slice: {}".format(i))
    arr = np.random.rand(cube_side, cube_side)
    t1 = time.time()
    dset[i,:,:] = arr
    t2 = time.time()
    print("   done ({:.2f}s)".format(t2 - t1))
    

print("done!")
print("Use: $hsls {} to view domain".format(filename))

f.close()
