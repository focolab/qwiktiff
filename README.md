# QwikTiff
Performant, lazy reader of large tiff datasets

# About
QwikTiff is a lightweight class for performant, lazy data access from large tiff stacks. It works by computing and storing the byte offsets for tiff pages, allowing direct page reads without file traversal.

Byte offsets are tabulated only once, when a tiff stack is first loaded. Subsequent ```QwikTiff``` objects that are reinstantiated from the saved parameters (usually from a json file) will be snappy!

QwikTiff is built on Cristoph Gohlke's [tifffile library](https://github.com/cgohlke/tifffile/blob/master/tifffile/tifffile.py).

# Usage
A ```QwikTiff``` object is instantiated by passing a (properly sorted) list of tiff files for one recording.
```python
qtf = QwikTiff(['file1.tiff', 'file2.tiff'])
qtf.to_json('qwiktiff.json')
```
Exporting ```to_json()``` will then store the page offsets. This only needs to be done once per dataset and could be automated by making an ingestion script.


For all subsequent uses, reload from json via
```python
qtf = QwikTiff.from_json('qwiktiff.json')
```

QwikTiff does not have bells and whistles, the main method is ```get_page()```.
```
qtf.get_page(0)     # fast
qtf.get_page(800)   # also fast
qtf.get_page(8000)  # you guessed it
```

That is about it! The rest is up to you :)

# Performance
In progress..

# Use cases
QwikTiff is useful for large tiff datasets (>10GB) where the time to traverse the file(s) and build a full page index is prohibitive. It is especially helpful for large datasets on network or HDD storage. QwikTiff ```get_page()``` calls can be used with [Dask](https://docs.dask.org/en/stable/) to construct large, lazy data arrays. Using QwikTiff to access raw data, GUI tools can exploit striding and caching strategies to allow faster scrubbing through huge datasets.

QwikTiff is not intended to replace or compete with modern, high performance data formats. These formats will most certainly outperform QwikTiff. But many researchers are hesitant to convert their primary data because it either requires doubled storage or deletion of the primary data.

QwikTiff will not give much of a performance boost for small datasets (a few GB), especially if stored on an SSD, but it also will not hamper performance. 
