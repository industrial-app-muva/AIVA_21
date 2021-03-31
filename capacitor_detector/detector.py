import concurrent.futures
import os

import cv2 as cv
from tqdm import tqdm

TEMPLATES_PATH = os.path.abspath(__file__).replace("detector.py", "templates")


class CapacitorDetector:

    def __init__(self):
        self.templates = self.__load_templates()

    @staticmethod
    def __load_templates():
        return [
            cv.imread(f'{TEMPLATES_PATH}/{template_file}', 1)
            for template_file in os.listdir(TEMPLATES_PATH)
        ]

    @staticmethod
    def __process_image(img, template, method=cv.TM_CCOEFF_NORMED, threshold=0.7):
        h, w = template.shape[0], template.shape[1]

        res = cv.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        if max_val > threshold:
            return [*max_loc, w, h]
        return None

    def detect(self, img):
        result_img, b_boxes = img.copy(), []

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures_process = [
                executor.submit(self.__process_image, result_img, template)
                for template in self.templates
            ]

            with tqdm(total=len(futures_process)) as progress_bar:
                for future in concurrent.futures.as_completed(futures_process):
                    bbox = future.result()
                    if bbox:
                        b_boxes.append(future.result())
                    progress_bar.update(1)

        for bbox in b_boxes:
            cv.rectangle(result_img,
                         (bbox[0], bbox[1]),
                         (bbox[0] + bbox[3], bbox[1] + bbox[2]),
                         (0, 0, 255), 5)

        return result_img, b_boxes
