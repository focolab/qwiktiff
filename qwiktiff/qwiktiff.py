
import json
import os
from tifffile import TiffFile, TiffPage

class QwikTiff():
    """Qwik lazy access for tiff datasets


    Attributes
    ----------
    files : list
        tiff files (must be correctly sorted)
    tifffiles : list
        instantiated TiffFile objects, one per file
    page_byte_offsets : list of lists
        page byte offsets, one list per file
    index : list
        index for all pages in the multifile stack. List elements are (ix, pbo)
        tuples where ix is the file index and pbo is the page byte offset
        (within the file)

    Methods
    -------
    get_page(): returns a TiffPage 
    to_dict(): serialize to a dict (useful if you want to embed the qwiktiff
        information into your own metadata container)
    to_json(): export to json
    from_json(): reload from json
    """
    def __init__(self, files, page_byte_offsets=None):
        self.files = files
        self.tifffiles = [TiffFile(f) for f in self.files]
        if page_byte_offsets:
            self.page_byte_offsets = page_byte_offsets
        else:
            print('computing page_byte_offsets')
            self.page_byte_offsets = [[p.offset for p in x.pages] for x in self.tifffiles]

        self.index = []
        for i, f in enumerate(self.files):
            for j in range(len(self.page_byte_offsets[i])):
                self.index.append((i, self.page_byte_offsets[i][j]))

    def get_page(self, i):
        _ = self.tifffiles[self.index[i][0]].filehandle.seek(self.index[i][1])
        return TiffPage(self.tifffiles[self.index[i][0]], index=0)

    def to_dict(self):
        return dict(files=self.files, page_byte_offsets=self.page_byte_offsets)

    def to_json(self, f='qwiktiff.json'):
        dd = self.to_dict()
        dd['files'] = [os.path.relpath(x, os.path.dirname(os.path.abspath(f))) for x in self.files]
        with open(f, 'w') as f:
            json.dump(dd, f, indent=2)
            f.write('\n')

    @classmethod
    def from_json(cls, f):
        with open(f) as jfopen:
            jd = json.load(jfopen)
        json_folder = os.path.dirname(f)
        jd['files'] = [os.path.abspath(os.path.join(json_folder, x)) for x in jd['files']]
        return cls(**jd)


if __name__ == "__main__":
    pass