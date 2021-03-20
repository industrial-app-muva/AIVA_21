import unittest
import requests

from capacitor_detector.detector import CapacitorDetector
from capacitor_detector.api import CapacitorDetectorAPI

class TestAPI(unittest.TestCase):
    def test_constructor(self):
        detector = CapacitorDetector()
        # TODO: Read same templates as detector and compare the lists
        self.assertEqual([], detector.templates)

    def test_process_img(self):
        detector = CapacitorDetector()
        # TODO: Read image and read bboxs of the image.
        _, bboxs = detector.detect(image)
        self.assertEqual([], bboxs)

class TestDetector(unittest.TestCase):
    def test_constructor(self):
        api = CapacitorDetectorAPI()
        # TODO: Read same templates as detector and compare the lists
        self.assertEqual([], api.detector.templates)

    def test_detect(self):
        api = CapacitorDetectorAPI()
        # TODO: Read image and read bboxs of the image.
        _, bboxs = api.process_img(image)
        self.assertEqual([], bboxs)

class TestApp(unittest.TestCase):
    def test_hello_world(self):
        pass

    def test_process_img_gui(self):
        pass

    def test_allowed_file(self):
        pass

    def test_parse_file_storage_2_numpy(self):
        pass

    def test_init_gui(self):
        pass


if __name__ == '__main__':
    unittest.main()
