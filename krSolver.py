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
	size = draw.textsize(text, font)
	print(size)
	draw.text((10, 3), text, font=font, fill=(0))

	return threshold(np.array(pil_img), .6), size

def threshold(grayscale, threshold):
	th, out = cv2.threshold(grayscale, threshold * 255, 255, cv2.THRESH_BINARY)
	return out

if __name__ == '__main__':
	filename = '../kingsreward_001.jpeg'
	alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	guess = 'xKQsdfsdf'
	best_ch = ''

	kr = threshold(cv2.imread(filename, cv2.IMREAD_GRAYSCALE), .6)

	# sc1, im1 = score(kr, generate_captcha('xKQ'))
	# sc2, im2 = score(kr, generate_captcha('xKQj'))
	# print sc1
	# print sc2
	# cv2.imshow("progress1", im1)
	# cv2.imshow("progress2", im2)
	# cv2.waitKey(0)

	while len(guess) < 5:
		base_score = score(kr, generate_captcha(guess))[0]
		min_score = 10e10
		guesses = []
		for ch in alphabet:
			ch_score, diff = score(generate_captcha(ch), generate_captcha(''))
			# print(ch_score)
			# cv2.imshow("progress", diff)
			# cv2.waitKey(0)
			
			guess_score = score(kr, generate_captcha(guess + ch))[0]

			gain = base_score - guess_score
			guesses.append(((ch_score - gain), gain, ch, ch_score))

			if (ch_score - gain) < min_score:
				min_score = (ch_score - gain)
				best_ch = ch

		guess += best_ch
		guesses.sort()
		for line in guesses:
			print(line)

		cv2.imshow("progress", score(kr, generate_captcha(guess))[1])
		cv2.waitKey(0)

		#print min_score

	print(guess)