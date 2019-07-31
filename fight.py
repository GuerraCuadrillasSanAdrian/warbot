#!/usr/bin/python3
from PIL import Image, ImageDraw, ImageFont

DEBUG = False

def print_debug(msg):
    if DEBUG:
        print(msg)

def unpack(line):
    instagram = ''
    try:
        name, instagram = line.split("@")
    except ValueError:
        name = line.split("@")[0]
    return (name, instagram)

def get_font(fontpath, size):
    return ImageFont.truetype(fontpath, size=size)

def get_centered(draw, value, font, W): 
    (w, h) = draw.textsize(value, font=font)
    return (W - w) / 2

def get_users(filename):
    userlist = []
    instadict = {}
    with open(filename, encoding='utf-8', errors='replace') as f:
        line = f.readline().rstrip()
        cnt = 0
        while line:
            cnt += 1
            name, instagram = unpack(line)
            if len(instagram):
                print_debug("%s %s: %s (@%s)" % (filename.split('.')[0].capitalize(), cnt, name, instagram))
                instadict[name] = instagram
            else:
                print_debug("%s %s: %s" % (filename.split('.')[0].capitalize(), cnt, name))
            userlist.append(name)
            line = f.readline().rstrip()
    return userlist, instadict


def initial_check():
    if input_check():
        print("[INFO] Data ok.")
    else:
        exit_error('Dead/alive files are not placed where they were expected. Exiting...')

def input_check():
    import os
    return os.path.isfile('alive.txt') and os.path.isfile('dead.txt')

def exit_error(msg):
    print("[ERROR] " + msg)
    exit(1)

def get_random_index(num_elements):
    import numpy as np
    return np.random.randint(num_elements)

def remove_line_from_file(filename, line_idx):
    with open(filename, "r", encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    cnt = 0
    with open(filename, "w", encoding='utf-8', errors='replace') as f:
        for line in lines:
            if cnt != line_idx:
                f.write(line)
            cnt += 1

def write_alive(idx):
    remove_line_from_file('alive.txt', idx)

def append_line(filename, name, idict):
    line = name
    if name in idict:
        line += '@' + idict[name]
    with open(filename, "a", encoding='utf-8', errors='replace') as f:
        f.write(line + '\n')

def write_dead(name, idict):
    append_line('dead.txt', name, idict)

def write_to_file(filename, value):
    with open(filename, "w+", encoding='utf-8', errors='replace') as f:
        f.write(value + '\n')

def finish_check(alivelist):
    if len(alivelist) == 1:
        print("[INFO] %s ganó la guerra, no hay nada más que hacer." % (alivelist[0]))
        exit(0)
    else:
        print("[INFO] Quedan %s cuadrillas con vida." % (len(alivelist)))

def resurrection(deadlist):
    import numpy as np
    # There is a 10% chance to come back to life.
    idx = None
    if not np.random.randint(11):
        idx = np.random.randint(len(deadlist))
        print("[RES!] %s ha vuelto. No estaban muertos, estaban de parranda!" % (deadlist[idx]))
    return idx

def get_round_n():
    filename = 'round.txt'
    try:
        with open(filename, 'r', encoding='utf-8', errors='replace') as f:
            round_n = int(f.readlines()[0].rstrip()) + 1
    except FileNotFoundError:
        round_n = 1
    write_to_file(filename, str(round_n))
    return round_n

def exit(errno=0):
    import sys
    sys.exit(errno)

def main():
    # Template settings
    W, H = (1080, 1440)
    (white_color, red_color, orange_color) = ('rgb(255, 255, 255)', 'rgb(255, 0, 0)', 'rgb(255, 165, 0)')
    normalFont = get_font('fonts/merienda.regular.ttf', 46) 
    bigFont = get_font('fonts/merienda.regular.ttf', 58)
    (rndx, rndy) = (865, 175)       # Round position
    (cuad1x, cuad1y) = (None, 325)  # Cuadrilla1 position
    (cuad2x, cuad2y) = (None, 485)  # Cuadrilla2 position
    (foto1x, foto1y) = (None, 585)  # Photo position
    (deadx, deady) = (None, 1020)   # Dead position
    (resx, resy) = (None, 1180)     # Resurrection msg position

    # Main code
    instadict = {}
    alive_f = 'alive.txt'
    dead_f = 'dead.txt'
    initial_check()
    alivelist, aliveinsta = get_users(alive_f)
    finish_check(alivelist)
    round_n = get_round_n()
    print_debug("[INFO] Ronda actual: %s" % (round_n))
    instadict.update(aliveinsta)
    deadlist, deadinsta = get_users(dead_f)
    instadict.update(deadinsta)
    print_debug("Choosing one from alive list...")
    idx = get_random_index(len(alivelist))
    idx2 = get_random_index(len(alivelist))
    if len(alivelist) <= 4:
        while idx == idx2:
            idx2 = get_random_index(len(alivelist))
    if idx == idx2:
        template = Image.open("templates/civil_1080x1440.png")
        draw = ImageDraw.Draw(template)
        print("[KILL] %s se ha desintegrado." % (alivelist[idx]))
    else:
        template = Image.open("templates/basic_1080x1440.png")
        draw = ImageDraw.Draw(template)
        draw.text((get_centered(draw, alivelist[idx], normalFont, W), cuad1y), alivelist[idx], fill=white_color, font=normalFont)
        draw.text((get_centered(draw, alivelist[idx2], normalFont, W), cuad2y), alivelist[idx2], fill=white_color, font=normalFont)
        print("[KILL] %s ha acabado con %s." % (alivelist[idx], alivelist[idx2]))
    write_alive(idx2)
    write_dead(alivelist[idx2], instadict)
    if len(alivelist) == 2:
        idx = 0 if alivelist[0] != alivelist[idx2] else 1  
        print("[INFO] %s ha ganado la guerra, ahora San Adrián le pertenece." % (alivelist[idx]))
        exit(0)
    # Draw over template
    draw.text((rndx, rndy), str(round_n), fill=white_color, font=bigFont)
    img = Image.open('photos/' + alivelist[idx2].replace(' ','').lower() + '.png', 'r')
    img_w, img_h = img.size
    offset = ((W - img_w) // 2, foto1y)
    template.paste(img, offset)
    draw.text((get_centered(draw, alivelist[idx2], normalFont, W), deady), alivelist[idx2], fill=red_color, font=normalFont)

    lucky = resurrection(deadlist)
    remaining_n = len(alivelist) - 1
    if lucky is not None:
        remove_line_from_file(dead_f, lucky)
        append_line(alive_f, deadlist[lucky], instadict)
        lucky_text = deadlist[lucky] + ' ha resucitado!'
        draw.text((get_centered(draw, lucky_text, normalFont, W), resy), lucky_text, fill=orange_color, font=normalFont)
        remaining_n += 1
    (remx, remy) = (495 if remaining_n > 9 else 510, 1320)      # Remaining position
    draw.text((remx, remy), str(remaining_n), fill=white_color, font=bigFont)
    template.save('/var/www/warbot/gc/round' + str(round_n) + '.png')
if __name__ == "__main__":
    main()
