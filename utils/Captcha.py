def random_color(c2, c1, c=0):
    rgbl=[c2, c1, c]
    random.shuffle(rgbl)
    return tuple(rgbl)
import random

from PIL import Image, ImageDraw, ImageFont
    
class Captcha:
	def buildCaptcha(self, size):
		letter = ""
		for i in range(size):
			letter += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

		return [letter, self.draw(letter)]

	def draw(self, text):
		x, y = 2, 2
		font = ImageFont.truetype("DroidSansMono.ttf", 14)
		img  = Image.new("RGB", (36, 17), (random_color(238, 255)))
		d = ImageDraw.Draw(img)
		for coordinate in [(x-1, y), (x+1, y), (x, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1)]:
			d.text(coordinate, text, font=font, fill=(255,0,0))

		d.text((x, y), text, font=font, fill=(random_color(10, 200, random.randint(220, 255))))
		return img