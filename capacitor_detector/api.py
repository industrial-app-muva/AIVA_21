from capacitor_detector.detector import CapacitorDetector
from capacitor_detector.extractor import MotherboardExtractor


class CapacitorDetectorAPI:
    def __init__(self):
        self.detector = CapacitorDetector()

    def process_img(self, img):
        motherboard_img = MotherboardExtractor.extract(img)
        return self.detector.detect(motherboard_img)
