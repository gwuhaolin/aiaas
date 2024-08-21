from unittest import TestCase

from . import ocr, ocr_http


class Test(TestCase):
    def test_ocr(self):
        print(ocr('/backup/xhs/66bff18b000000000503046b/0.webp'))


    def test_ocr_http(self):
        print(ocr_http('/backup/xhs/66bff18b000000000503046b/0.webp'))
