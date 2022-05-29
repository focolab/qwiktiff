#!/usr/bin/env bash

# best to run lines manually instead of running bash script
conda create -n qwiktiff python pip

# activate env (use source activate for unix systems)
activate qwiktiff

# install other packages (TODO append as necessary)
# note prefer tifffile to pylibtiff because the former supports writing with LZMA compression
# and the latter doesn't support any compression
conda install tifffile -c conda-forge


