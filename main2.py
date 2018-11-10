import numpy as np
import cv2
import matplotlib.pyplot as plt 
import time
'''
def CoordinateCreator(img, line_parameters):
    slope, intercept = line_parameters
    y1 = img.shape[0]
    y2 = int(y1*(4/5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1,y1,x2,y2])

def AverageSlopeIntercept(img, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1,y1),(x2,y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_avg = np.average(left_fit, axis=0)
    right_fit_avg = np.average(right_fit, axis=0)
    left_line = CoordinateCreator(img, left_fit_avg)
    righ_line = CoordinateCreator(img, right_fit_avg)
    return np.array([left_line, righ_line])
'''
def Canny(img):
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    img = cv2.GaussianBlur(img,(3,3),0)
    img = cv2.Canny(img,35,105)
    return img

def DispLines(img, lines):
    line_img = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_img, (x1,y1), (x2,y2), (255,0,0), 10)
    return line_img

def Roi(img):
    #100,500:  500,500 : 300,280
    height = img.shape[0]
    polygon = np.array([[(100,height-40), (500, height-40), (300,340)]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask,polygon,255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

def main():
    #width = 600
    #height = 337
    #dim = (width,height)
    count = 1

    while True:
        img_name = 'lane/'+ '{:04}'.format(count) + '.jpg'
        frame = cv2.imread(img_name, 1)
        #frame = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        canny = Canny(frame)
        roi_img = Roi(canny)
        lines = cv2.HoughLinesP(roi_img, 2, np.pi/180, 80, np.array([]), minLineLength=7, maxLineGap=5)
        line_img = DispLines(frame, lines)
        detected_lines = cv2.addWeighted(frame, 0.8, line_img, 1, 1)
        cv2.imshow('Lane Detection', detected_lines)
        cv2.imshow('Original', frame)
        time.sleep(0.2)
        k = cv2.waitKey(5) & 0xFF 
        if k == 27 or count == 699:
            break
        
        count += 1
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()