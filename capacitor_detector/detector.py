
class CapacitorDetector:

    def __init__(self):
        self.templates = self.__load_templates()
    
    def __load_templates(self):
        pass
        # TODO: Load templates

    def detect(self, img, method = 'cv.TM_CCOEFF'):
        result_img, bboxs = img.copy(), []
        
        for template in self.templates:
            w, h = template.shape[::-1]
            
            # Apply template Matching
            res = cv.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            top_left = max_loc

            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv.rectangle(result_img, top_left, bottom_right, 255, 2)

            bboxs.append([**top_left, w, h])

        # TODO: Filter results

        return result_img, bboxs
        