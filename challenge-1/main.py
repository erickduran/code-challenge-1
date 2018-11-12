import numpy as np
import cv2
import time
import math

def canny(img):
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    img = cv2.GaussianBlur(img,(3,3),0)
    img = cv2.Canny(img,35,105)
    return img

def region_of_interest(img):
    height = img.shape[0]
    polygon = np.array([[(100,height-40), (500, height-40), (300,340)]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask,polygon,255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

def add_lines(img, lines, last):
    overlay = img.copy()
    output = img.copy()
    if lines is not None:
        left = False
        right = False
        left_max = 0
        right_max = 0
        left_max_line = None
        right_max_line = None
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            size = math.sqrt(((x1-x2)**2)+((y1-y2)**2))
            if x1 <= 320 and x2 <= 320:
                left = True
                if size > left_max:
                    left_max = size
                    left_max_line = line
            if x1 > 320 and x2 > 320:
                right = True
                if size > right_max:
                    right_max = size
                    right_max_line = line
        if left and right:
            lines = []
            lines.append(left_max_line)
            lines.append(right_max_line)
            x1_0, y1_0, x2_0, y2_0 = left_max_line.reshape(4)
            x1_1, y1_1, x2_1, y2_1 = right_max_line.reshape(4)  
            points = np.array([[x1_0,y1_0],[x2_0,y2_0],[x1_1,y1_1],[x2_1,y2_1]])
            cv2.fillPoly(overlay, np.int32([points]), (0,255,0))
            alpha = 0.3
            cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
            cv2.line(output, (x1_0,y1_0), (x2_0,y2_0), (0,255,0), 10)
            cv2.line(output, (x1_1,y1_1), (x2_1,y2_1), (0,255,0), 10)
            # print('both lines')
            last = lines
        else:
            if last is not None:
                left_max_line = last[0]
                right_max_line = last[1]
                x1_0, y1_0, x2_0, y2_0 = left_max_line.reshape(4)
                x1_1, y1_1, x2_1, y2_1 = right_max_line.reshape(4)  
                points = np.array([[x1_0,y1_0],[x2_0,y2_0],[x1_1,y1_1],[x2_1,y2_1]])
                cv2.fillPoly(overlay, np.int32([points]), (0,255,0))
                alpha = 0.3
                cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
                cv2.line(output, (x1_0,y1_0), (x2_0,y2_0), (0,255,0), 10)
                cv2.line(output, (x1_1,y1_1), (x2_1,y2_1), (0,255,0), 10)
                # print('replaced with last')
            else:
                cv2.putText(output, 'Locating lanes...',(300, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
    return output, last

def main():
    count = 1
    last = None
    while True:
        img_name = 'lane/'+ '{:04}'.format(count) + '.jpg'
        frame = cv2.imread(img_name, 1)
        canny_img = canny(frame)
        roi_img = region_of_interest(canny_img)
        lines = cv2.HoughLinesP(roi_img, 2, np.pi/180, 80, np.array([]), minLineLength=7, maxLineGap=5)
        line_img, l = add_lines(frame, lines, last)
        last = l
        detected_lines = cv2.addWeighted(frame, 0.8, line_img, 1, 1)
        cv2.imshow('Lane Detection', detected_lines)
        # cv2.imshow('Original', canny_img)
        # time.sleep(0.05)
        count += 1
        k = cv2.waitKey(5) & 0xFF 
        if k == 27 or count == 699:
            break
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()