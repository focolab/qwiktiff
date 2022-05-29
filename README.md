# QwikTiff
Performant, lazy reader of large tiff datasets

# About
QwikTiff is a lightweight tool for performant, lazy data access from large tiff stacks. It works by computing and storing the byte offsets for tiff pages, allowing direct page reads without file traversal.

Byte offsets are tabulated only once, when a tiff stack is first loaded. Subsequent ```QwikTiff``` objects that are reinstantiated from the saved parameters (usually from a json file) will be snappy!

QwikTiff is built on Cristoph Gohlke's tifffile library
(https://github.com/cgohlke/tifffile/blob/master/tifffile/tifffile.py)

# Usage

A ```QwikTiff``` object is instantiated by passing a (properly sorted) list of tiff files.
```python
qtf = QwikTiff(['file1.tiff', 'file2.tiff'])
qtf.to_json('qwiktiff.json')
```
This only needs to be done once per dataset, and could be automated for multiple datasets by making an ingestion script.


For all subsequent uses, reload from json 
```python
qtf = QwikTiff.from_json('qwiktiff.json')
```

QwikTiff does not have bells and whistles, the main method is ```get_page()```
```
qtf.get_page(0)     # fasttt
qtf.get_page(800)   # also fastttt
```

That is about it! The rest is up to you :)

# Performance


# Use cases
QwikTiff is useful for large tiff datasets (>10GB) where the time to count pages and build a full page index is prohibitive. This file traversal can be horrendously slow for large datasets on network or HDD storage. Using QwikTiff, analysis and GUI tools can build a full page index without any file traversal. Furthermore, GUI tools can exploit striding and caching strategies to allow faster scrubbing through huge datasets.

QwikTiff is not intended to replace or compete with modern, high performance data formats. These formats will most certainly outperform QwikTiff. But many people are hesitant to convert their primary data because it either requires i. doubled storage ii. deletion of the primary data.

QwikTiff won't give much of a performance boost for small datasets (a few GB), especially if stored on an SSD.

Pycromanager now uses a tiff format that declares byte offsets



