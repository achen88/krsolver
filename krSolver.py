import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image

def score(img1, img2):
	diff = np.zeros(np.shape(img1))

	for i in range(len(img1)):
		for j in range(len(img1[0])):
			diff[i,j] = abs(int(img1[i,j]) - int(img2[i,j]))

	return np.sum(diff), diff

def generate_captcha(text):
	#new grayscale canvas
	pil_img = Image.new("L", (200, 58), "white")

	#draw text
	draw = ImageDraw.Draw(pil_img)
	font = ImageFont.truetype("/Library/Fonts/Microsoft/Verdana.ttf", 37)
	draw.text((10, 3), text, font=font, fill=(0))

	return np.array(pil_img)

def threshold(grayscale, threshold):
	th, out = cv2.threshold(grayscale, threshold * 255, 255, cv2.THRESH_BINARY)
	return out

if __name__ == '__main__':
	filename = 'kingsreward_002.jpeg'
	alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	min_score = 10e10
	guess = ''
	best_ch = ''

	kr = threshold(cv2.imread(filename, cv2.IMREAD_GRAYSCALE), .6)

	while len(guess) < 5:
		for ch in alphabet:
			if score(kr, generate_captcha(guess + ch))[0] < min_score:
				min_score = score(kr, generate_captcha(guess + ch))[0]
				best_ch = ch
		guess += best_ch

		cv2.imshow("progress", score(kr, generate_captcha(guess))[1])
		cv2.waitKey(0)

		print min_score

	print guess