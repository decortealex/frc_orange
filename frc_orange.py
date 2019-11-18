import numpy as np
import cv2

cam = cv2.VideoCapture(0)

lower_threshold = np.zeros(3)
upper_threshold = np.zeros(3)

bound_val = 0


def change_exposure(exposure_val):
    cam.set(cv2.CAP_PROP_EXPOSURE, exposure_val)


def change_brightness(brightness_val):
    cam.set(cv2.CAP_PROP_BRIGHTNESS, brightness_val)


def change_contrast(contrast_val):
    cam.set(cv2.CAP_PROP_CONTRAST, contrast_val)


def change_saturation(saturation_val):
    cam.set(cv2.CAP_PROP_SATURATION, saturation_val)

def invert_image(image):
    return cv2.bitwise_not(image)


def flip_image_vert(image):
    return cv2.flip(image, 0)


def flip_image_hor(image):
    return cv2.flip(image, 1)


def set_hsv_bounds(lower_bound, upper_bound):
    lower_threshold = lower_bound
    upper_threshold = upper_bound


def set_thresh_bound(thresh_val):
    bound_val = thresh_val


def draw_cnts_hsv(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_threshold, upper_threshold)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) [-2]

    if len(cnts) > 0:
        area = max(cnts, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(area)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


def draw_cnts(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) [-2]

    if len(cnts) > 0:
        area = max(cnts, key=cv2.contourArea)
        rect = cv2.minAreaRect(area)
        cv2.imshow('threshold', thresh)
        return cv2.boxPoints(rect)
        # print(x,y,w,h)
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    

while(True):
    ret, frame = cam.read()

    set_thresh_bound(210)
    box = draw_cnts(frame)
    box = np.int0(box)

    cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cv2.imshow('video', frame)

cam.release()
cv2.destroyAllWindows()
