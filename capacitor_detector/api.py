from detector import CapacitorDetector

class CapacitorDetectorAPI:
    def __init__(self):
        self.detector = CapacitorDetector()

    def process_img(self, img):
        return self.detector.detect(img)

    