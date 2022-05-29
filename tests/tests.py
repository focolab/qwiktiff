import os
import shutil
import time
from tifffile import TiffWriter, TiffFile
import numpy as np
from qwiktiff.qwiktiff import QwikTiff

class Test00:
    def setUp(self):
        rng = np.random.default_rng(42)
        os.makedirs('test00', exist_ok=True)
        self.f1 = 'test00/tiff1.tiff'
        self.f2 = 'test00/tiff2.tiff'
        self.json_file = 'test00/qwiktiff.json'
        with TiffWriter(self.f1) as tif:
            for i in range(10):
                arr = rng.integers(0, 254, (1000, 1000)).astype(np.uint8)
                tif.write(arr) 
        with TiffWriter(self.f2) as tif:
            for i in range(10):
                arr = rng.integers(0, 254, (1000, 1000)).astype(np.uint8)
                tif.write(arr)

    def test00(self):
        """test multifile indexing"""
        qtf = QwikTiff([self.f1, self.f2])
        pg5 = qtf.get_page(5)
        pg15 = qtf.get_page(15)
        assert pg5.shape == (1000, 1000)
        assert pg15.shape == (1000, 1000)

    def test01(self):
        """test json export/import"""
        qtf = QwikTiff([self.f1, self.f2])
        qtf.to_json(self.json_file)
        qtf2 = QwikTiff.from_json(self.json_file)
        d1 = qtf.get_page(5).asarray()
        d2 = qtf2.get_page(5).asarray()
        assert (d1==d2).all()

    def test02(self):
        """performance"""
        rng = np.random.default_rng(42)
        self.f1 = 'test00/tiff1.tiff'
        self.f2 = 'test00/tiff2.tiff'
        self.json_file = 'test00/qwiktiff.json'
        with TiffWriter(self.f1) as tif:
            for i in range(2001):
                arr = rng.integers(0, 254, (1000, 1000)).astype(np.uint8)
                tif.write(arr) 
        with TiffWriter(self.f2) as tif:
            for i in range(2001):
                arr = rng.integers(0, 254, (1000, 1000)).astype(np.uint8)
                tif.write(arr)

        # TiffFile
        t00 = time.time()
        data1 = TiffFile(self.f1).pages[2000].asarray()
        t01 = time.time()

        page_byte_offsets = QwikTiff([self.f1]).page_byte_offsets

        # QwikTiff
        t02 = time.time()
        data2 = QwikTiff([self.f2], page_byte_offsets=page_byte_offsets).get_page(2000).asarray()
        t03 = time.time()

        print('======== performance ========')
        print('TiffFile: %8.4f' % (t01-t00))
        print('QwikTiff: %8.4f' % (t03-t02))
        print('=============================')

    def tearDown(self):
        shutil.rmtree('test00')

    def run(self):
        self.setUp()
        self.test00()
        self.test01()
        self.test02()
        self.tearDown()

if __name__ == "__main__":
    Test00().run()
