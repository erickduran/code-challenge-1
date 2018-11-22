import cv2
import numpy as np
import time
	
def main():
	count = 0
	alpha = 0.3
	fgbg = cv2.createBackgroundSubtractorMOG2()
	kernel = np.ones((3,3),np.uint8)

	while True:
		img_name = 'res/breakdance/'+ '{:05}'.format(count) + '.jpg'
		frame = cv2.imread(img_name, 1)

		overlay = frame.copy()
		output = frame.copy()

		if count == 0:
			frame[:,0:196] = 0
			frame[:,560:854] = 0
			frame[402:480,:] = 0

		fgmask = fgbg.apply(frame)
		fgmask = cv2.erode(fgmask, None, iterations=2)
		fgmask = cv2.dilate(fgmask, None, iterations=2)
		fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

		sure_bg = cv2.dilate(fgmask,kernel,iterations=1)
		dist_transform = cv2.distanceTransform(fgmask,cv2.DIST_L2,5)			
		_, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

		sure_fg = np.uint8(sure_fg)
		unknown = cv2.subtract(sure_bg,sure_fg)

		ret, markers = cv2.connectedComponents(sure_fg)
		markers = markers+1
		markers[unknown==255] = 0
		markers = cv2.watershed(frame,markers)
		# frame[markers == -1] = [255,0,0]

		unknown = cv2.medianBlur(unknown, 11)
		unknown = cv2.morphologyEx(unknown, cv2.MORPH_OPEN, kernel)
		unknown = cv2.morphologyEx(unknown, cv2.MORPH_CLOSE, kernel)

		_, contours, _ = cv2.findContours(unknown,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		
		for contour in contours:
			area = cv2.contourArea(contour)
			if area > 500:
				cv2.fillPoly(overlay, np.int32([contour]), (0,255,0))
				cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

		if count != 0:
			cv2.imshow('frame', output)

		time.sleep(1)
		count += 1

		k = cv2.waitKey(5) & 0xFF 
		if k == 27 or count == 70:
			break

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()