import cv2
import numpy as np
import time

def main():
	width = 600
	height = 337
	dim = (width, height)
	count = 1
	
	while True:
		img_name = 'lane/'+ '{:04}'.format(count) + '.jpg'
		image = cv2.imread(img_name, 1)
		frame = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

		cv2.imshow('frame', frame)
		time.sleep(0.5)
		k = cv2.waitKey(5) & 0xFF

		if k == 27 or count == 699:
			break
			
		count+=1

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
