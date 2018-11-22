import cv2
import numpy as np
	
def main():

	fgbg = cv2.createBackgroundSubtractorMOG2()
	kernel = np.ones((3,3),np.uint8)

	# img = cv2.imread('image.png')
	cap = cv2.VideoCapture('video.mp4')
	while True:
		ret, frame = cap.read()

		fgmask = fgbg.apply(frame)
		median = cv2.medianBlur(fgmask, 3)
		
		cv2.imshow('frame', median)

		# time.sleep(0.05)

		k = cv2.waitKey(5) & 0xFF 
		if k == 27:
			break

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()