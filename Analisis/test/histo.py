import unittest
from Analisis.script.histo import ColorExtract


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

        path = '/Users/riccardotesta_1/progetti-sviluppo-codice/Biennale/media/pic_folder/opere/preview/1._Aérius_1_thumbnail_UuhBztB.jpg'
        ce = ColorExtract()
        ce.get_colorspace(path)


if __name__ == '__main__':
    unittest.main()
