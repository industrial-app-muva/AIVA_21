import cv2 as cv
from tqdm import tqdm

import os

TEMPLATES_PATH = 'capacitor_detector/templates'


class CapacitorDetector:

    def __init__(self):
        self.templates = self.__load_templates()

    @staticmethod
    def __load_templates():
        return os.listdir(TEMPLATES_PATH)

    def detect(self, img, method=cv.TM_CCOEFF_NORMED, threshold=0.9):
        result_img, b_boxes = img.copy(), []

        for template_file in tqdm(self.templates):
            template = cv.imread(f'{TEMPLATES_PATH}/{template_file}', 1)
            h, w = template.shape[0], template.shape[1]
        
            # Apply template Matching
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            # print(max_val)
            if max_val > threshold:
                top_left = max_loc
            
                bottom_right = (top_left[0] + h, top_left[1] + w)
                cv.rectangle(result_img, top_left, bottom_right, 255, 2)
            
                b_boxes.append([*top_left, w, h])
        
            # TODO: Filter Non-Maxima supression

        return result_img, b_boxes
