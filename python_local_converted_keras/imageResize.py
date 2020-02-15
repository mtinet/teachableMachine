import cv2
import numpy as np

img = cv2.imread('image/test_photo.jpg')
cv2.imshow('img', img)
res = cv2.resize(img, dsize=(54, 140), interpolation=cv2.INTER_CUBIC)
cv2.imshow('res', res)

cv2.waitKey(0)
cv2.destroyAllWindows()
