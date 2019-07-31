#!/usr/bin/python3

def get_font(fontpath, size):
    return ImageFont.truetype(fontpath, size=size)

def get_centered(draw, value, font, W):
    (w, h) = draw.textsize(value, font=font)
    return (W - w) / 2

from PIL import Image, ImageDraw, ImageFont
template = Image.open("templates/basic_1080x1440.jpg")
W, H = (1080, 1440)
white_color = 'rgb(255, 255, 255)'

# Font, position and content
#myFont = ImageFont.truetype('fonts/MarkerNotes.ttf', size=46)
#myFont = ImageFont.truetype('fonts/merienda.regular.ttf', size=46)
normalFont = get_font('fonts/merienda.regular.ttf', 46)
bigFont = get_font('fonts/merienda.regular.ttf', 58)
round_n = 7
winner_name = 'La Cofradía del Canalillo'
loser_name = 'Peña La Toñi'
remaining_n = 11

(rndx, rndy) = (865, 175)       # Round position
(cuad1x, cuad1y) = (None, 325)  # Cuadrilla1 position
(cuad2x, cuad2y) = (None, 485)  # Cuadrilla2 position
(foto1x, foto1y) = (None, 585)  # Photo position
(deadx, deady) = (None, 1020)    # Dead position
(resx, resy) = (None, 1180)     # Resurrection msg position
(remx, remy) = (495 if remaining_n > 9 else 510, 1320)      # Remaining position

# Draw over template
draw = ImageDraw.Draw(template)
draw.text((rndx, rndy), str(round_n), fill=white_color, font=bigFont)
draw.text((get_centered(draw, winner_name, normalFont, W), cuad1y), winner_name, fill=white_color, font=normalFont)
draw.text((get_centered(draw, loser_name, normalFont, W), cuad2y), loser_name, fill=white_color, font=normalFont)
# Photo
img = Image.open('photos/' + loser_name.replace(' ','').lower() + '.png', 'r')
img_w, img_h = img.size
offset = ((W - img_w) // 2, foto1y)
template.paste(img, offset)
draw.text((get_centered(draw, loser_name, normalFont, W), deady), loser_name, fill=white_color, font=normalFont)
# TODO: Resurection
draw.text((remx, remy), str(remaining_n), fill=white_color, font=bigFont)

template.save('results/round' + str(round_n) + '.png')
