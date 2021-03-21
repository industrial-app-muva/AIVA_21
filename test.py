import unittest
import os
import sys

from capacitor_detector.api import CapacitorDetectorAPI
from capacitor_detector.detector import CapacitorDetector

import cv2 as cv


class TestDetector(unittest.TestCase):
    def test_constructor(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        detector = CapacitorDetector()
        templates = os.listdir('capacitor_detector/templates')

        self.assertEqual(len(templates), len(detector.templates))

        for t1, t2 in zip(templates, detector.templates):
            self.assertEqual(t1, t2)

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_process_img(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        detector = CapacitorDetector()
        image = cv.imread('static/image/rec1-3.jpg')
        
        result_img, bboxs = detector.detect(image)

        self.assertGreater(len(bboxs), 0)

        for bbox in bboxs:
            self.assertEqual(4, len(bbox))

        self.assertEqual(result_img.shape, image.shape)

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')


class TestAPI(unittest.TestCase):
    def test_constructor(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        api = CapacitorDetectorAPI()
        templates = os.listdir('capacitor_detector/templates')
        
        self.assertEqual(len(templates), len(api.detector.templates))

        for t1, t2 in zip(templates, api.detector.templates):
            self.assertEqual(t1, t2)

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_process_img(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        api = CapacitorDetectorAPI()
        image = cv.imread('static/image/rec1-3.jpg')
        
        result_img, bboxs = api.process_img(image)

        self.assertGreater(len(bboxs), 0)

        for bbox in bboxs:
            self.assertEqual(4, len(bbox))

        self.assertEqual(result_img.shape, image.shape)

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_precission(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        api = CapacitorDetectorAPI()
        image = cv.imread('static/image/rec1-3.jpg')
        
        result_img, bboxs = api.process_img(image)

        # The detector must detect more than 20 capactiors
        self.assertGreaterEqual(len(bboxs), 20)

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')


if __name__ == '__main__':
    unittest.main()
