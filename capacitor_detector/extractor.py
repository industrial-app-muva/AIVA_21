import numpy as np
import cv2 as cv

class MotherboardExtractor:
    @staticmethod
    def __crop_rect(img, rect):
        # get the parameter of the small rectangle
        center, size, angle = rect[0], rect[1], rect[2]
        center, size = tuple(map(int, center)), tuple(map(int, size))

        # get row and col num in img
        height, width = img.shape[0], img.shape[1]

        # calculate the rotation matrix
        M = cv.getRotationMatrix2D(center, angle, 1)
        # rotate the original image
        img_rot = cv.warpAffine(img, M, (width, height))

        # now rotated rectangle becomes vertical, and we crop it
        img_crop = cv.getRectSubPix(img_rot, size, center)

        return img_crop

    @staticmethod
    def extract(img):
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        ret,th1 = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        th1 = cv.dilate(th1, kernel, iterations = 1)

        contours, hierarchy = cv.findContours(th1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key = cv.contourArea)
        rect = cv.minAreaRect(cnt)

        return MotherboardExtractor.__crop_rect(img, rect)
