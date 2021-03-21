import cv2 as cv

import os
import concurrent.futures

from tqdm import tqdm

TEMPLATES_PATH = 'capacitor_detector/templates'


class CapacitorDetector:

    def __init__(self):
        self.templates = self.__load_templates()

    @staticmethod
    def __load_templates():
        return os.listdir(TEMPLATES_PATH)

    def __process_image(self, img, template, method=cv.TM_CCOEFF_NORMED, threshold=0.7):
        h, w = template.shape[0], template.shape[1]
    
        res = cv.v(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        if max_val > threshold:
            bottom_right = (max_loc[0] + h, max_loc[1] + w)
        
            return [*max_loc, w, h]
        return None

    def detect(self, img):
        result_img, bboxes = img.copy(), []

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures_process = [executor.submit(self.__process_image, img, cv.imread(f'{TEMPLATES_PATH}/{template_file}', 1)) 
                               for template_file in self.templates]

            with tqdm(total=len(futures_process)) as pbar:
                for future in concurrent.futures.as_completed(futures_process):
                    bbox = future.result()
                    if bbox:
                        bboxes.append(future.result())
                    pbar.update(1)

        for bbox in bboxes:
            cv.rectangle(result_img, (bbox[0], bbox[1]), (bbox[0] + bbox[3], bbox[1] + bbox[2]), 255, 2)
        
        return result_img, bboxes
