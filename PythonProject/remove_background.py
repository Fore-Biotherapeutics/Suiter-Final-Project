import cv2 as cv
import numpy as np


def main():
    img = cv.imread('standing_dude.JPG')
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    rect = (83, 40, 451, 678)
    cv.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]
    cv.imshow("", img)
    cv.waitKey()


if __name__ == '__main__':
    main()