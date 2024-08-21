import os
from unittest import TestCase
from . import txt2mp3, texts2srt

class Test(TestCase):
    def test_txt2mp3(self):
        txt2mp3("我现在还没完成的功能，你先用其他方式吧", "hello.mp3", 3000)

    def test_texts2srt(self):
        texts2srt([
            '我有145元钱',
            '1-3岁宝宝👶',
        ], os.getcwd())
