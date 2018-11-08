import cv2
import numpy as np
import time

size = 3
kernel_minus45 = np.zeros((size,size), np.float32)

kernel_minus45[:,:] = -1

for i in range(0, size):
	kernel_minus45[i,i] = 2

kernel_plus45 = np.zeros((size,size), np.float32)

kernel_plus45[:,:] = -1
kernel_plus45[2,0] = 2
kernel_plus45[1,1] = 2
kernel_plus45[0,2] = 2

def main():
	width = 600
	height = 337
	dim = (width, height)
	count = 1

	lower_bound = np.uint8([200, 200, 200])
	upper_bound = np.uint8([255, 255, 255])
	
	while True:
		img_name = 'lane/'+ '{:04}'.format(count) + '.jpg'
		image = cv2.imread(img_name, 1)
		frame = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
		frame[0:240, 0:600] = 0
		frame[320:337, 0:600] = 0

		median = cv2.medianBlur(frame,9)
		frame_canny = cv2.Canny(median,50,50)

		plus45 = cv2.filter2D(frame_canny,-1, kernel_plus45)
		minus45 = cv2.filter2D(frame_canny,-1, kernel_minus45)

		result = plus45 + minus45
		median = cv2.medianBlur(result,3)
		cv2.imshow('frame', minus45)
		time.sleep(0.1)
		k = cv2.waitKey(5) & 0xFF

		if k == 27 or count == 699:
			break
			
		count+=1

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
