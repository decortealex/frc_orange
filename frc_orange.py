from __future__ import division 
import numpy as np
import cv2

cam = cv2.VideoCapture(0)

bound_val = 200
calibration_point = [0, 0]

# this is an opencv specific handler for mouse click events
def set_center(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global calibration_point
        calibration_point = [x, y]
        # print(calibration_point)


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


def set_thresh_bound(thresh_val):
    bound_val = thresh_val


def draw_cnts(image):
    global frame
    frame = image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(image, bound_val, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) [-2]

    if len(cnts) > 0:
        area = max(cnts, key=cv2.contourArea)
        # print(get_percentage(image, cv2.findNonZero(thresh)))
        rect = cv2.minAreaRect(area)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        
        # get_cnt_area(box)
        # cv2.imshow('threshold', thresh)
        # print(box)
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
        return box
        # print(x,y,w,h)   
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


def get_percentage(image, pix_in_contour):
    return (pix_in_contour.size / image.size) * 100    


def target_dist_to_center(target):
    if target is not None:
        target_coord = center_of_cnt(target)
        dist_to_center = (calibration_point[0] - target_coord[0], target_coord[1] - calibration_point[1])
        print(dist_to_center)


def center_of_cnt(box):
    if box is not None:
        mid_x = ((abs(box[2][0] - box[1][0])) / 2) + abs(box[0][0])
        mid_y = abs(box[0][1]) - (abs(box[1][1] -  box[0][1]) / 2)
        return [mid_x, mid_y]


while(True):
    ret, frame = cam.read()
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', set_center)

    # print(calibration_point)

    set_thresh_bound(200)
    box = draw_cnts(frame)
    cnts_center = center_of_cnt(box)
    # print(cnts_center)
    target_dist_to_center(box)
    # cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cv2.imshow('image', frame)

cam.release()
cv2.destroyAllWindows()
