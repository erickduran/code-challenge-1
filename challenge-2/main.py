import cv2
import numpy as np
	
# add database to res/ folder inside this one
def main():
	# img = cv2.imread('image.png')
	count = 1
	while True:
		img_name = 'res/girl/'+ '{:05}'.format(count) + '.jpg'
		frame = cv2.imread(img_name, 1)
		
		cv2.imshow('frame', frame)

		# time.sleep(0.05)
		count += 1

		k = cv2.waitKey(5) & 0xFF 
		if k == 27 or count == 699:
			break

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()