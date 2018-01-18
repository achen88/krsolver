import numpy as np
import cv2
import requests
from PIL import ImageFont, ImageDraw, Image
from io import BytesIO

#filename = './data/kingsreward_000.jpeg'

def score(img1, img2):
	diff = np.zeros(np.shape(img1))

	for i in range(len(img1)):
		for j in range(len(img1[0])):
			diff[i,j] = abs(int(img1[i,j]) - int(img2[i,j]))

	return np.sum(diff), diff

def generate_captcha(text):
	offset = [10, 3]

	#new grayscale canvas
	pil_img = Image.new("L", (200, 58), "white")

	#draw text
	draw = ImageDraw.Draw(pil_img)
	font = ImageFont.truetype("/Library/Fonts/Microsoft/Verdana.ttf", 37)
	for ch in text:
		draw.text(offset, ch, font=font, fill=(0))
		offset[0] += draw.textsize(ch, font)[0]

	return threshold(np.array(pil_img), .6)

def threshold(grayscale, threshold):
	th, out = cv2.threshold(grayscale, threshold * 255, 255, cv2.THRESH_BINARY)
	return out

def solve(cookie, url):
	cookies = dict(PHPSESSID=cookie)
	r = requests.get(url, cookies=cookies)
	img = Image.open(BytesIO(r.content))
	kr = threshold(cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY), .6)

	alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	guess = ''

	#kr = threshold(cv2.imread(filename, cv2.IMREAD_GRAYSCALE), .6)

	# sc1, im1 = score(kr, generate_captcha('xKQ'))
	# sc2, im2 = score(kr, generate_captcha('xKQj'))
	# print(sc1)
	# print(sc2)
	# cv2.imshow("progress1", im1)
	# cv2.imshow("progress2", im2)
	# cv2.waitKey(0)

	while len(guess) < 5:
		base_score = score(kr, generate_captcha(guess))[0]
		max_usage = 0
		max_gain = 0
		guesses_usage = {}
		guesses_scores = {}
		for ch in alphabet:
			ch_score, diff = score(generate_captcha(ch), generate_captcha(''))
			# print(ch_score)
			# cv2.imshow("progress", diff)
			# cv2.waitKey(0)
			
			guess_score = score(kr, generate_captcha(guess + ch))[0]

			gain = base_score - guess_score
			guesses_usage[ch] = gain/ch_score if gain <= ch_score else 0
			guesses_scores[ch] = gain if gain > 0 else 0

			max_usage = max(max_usage, gain/ch_score)
			max_gain = max(max_gain, gain)

		final = {}

		max_val = max(guesses_scores.values()) + .1
		for ch in guesses_scores:
			guesses_scores[ch] /= max_val

		for ch in alphabet:
			final[ch] = .35 * guesses_usage[ch] + .65 * guesses_scores[ch]
		
		# print(sorted(guesses_usage.items(), key=lambda x: x[1]))
		# print(sorted(guesses_scores.items(), key=lambda x: x[1]))
		# print(sorted(final.items(), key=lambda x: x[1]))
		guess += max(final.items(), key=lambda x: x[1])[0]
		# cv2.imshow("progress", score(kr, generate_captcha(guess))[1])
		# cv2.waitKey(0)

		#print(min_score)

	return guess

if __name__ == '__main__':
	#solve()
	pass