import argparse
import os
from os.path import abspath, dirname
import re

import numpy as np
import cv2

def hex2bgr(hex):
    nohash = re.sub(r'^#','',hex)
    r = int(nohash[0:2], 16)
    g = int(nohash[2:4], 16)
    b = int(nohash[4:6], 16)
    return (b,g,r)


parser = argparse.ArgumentParser("Make a custom deck of playing cards")
parser.add_argument('input', type=str, nargs='?', default='standard/input.txt', help='Input file with keywords/values')
args = parser.parse_args()

cfg = {}
with open(args.input, 'r') as key_val:
    for line in key_val:
        nocomment = re.sub(r'#.*', '', line)
        kv = nocomment.split()
        if len(kv) == 2:
            key, val = kv
            if re.search(r'_[HW]$', key) or key=='DPI':
                cfg[key] = float(val)
            else:
                cfg[key] = val
os.chdir(dirname(args.input))

# determine pip placement for non-face cards
pip_nx = round(cfg['PIP_W']*cfg['DPI'])
pip_ny = round(cfg['PIP_H']*cfg['DPI'])
pip_dx = pip_nx / 6  # let these be float and round later
pip_dy = pip_ny / 8
pip_w = int(pip_dx)
pip_h = int(pip_dy)

pip_dict = {}
pip_dict[2] = ( (3,1), (3,7) )
pip_dict[3] = ( (3,1), (3,7), (3,4) )  # two, plus the middle
pip_dict[4] = ( (1,1), (5,1), (1,7), (5,7) ) # four corners
pip_dict[5] = ( (1,1), (5,1), (1,7), (5,7), (3,4) ) # four, plus the middle
pip_dict[6] = ( (1,1), (5,1), (1,7), (5,7), (1,4), (5,4) ) # four, plus 2 middles
pip_dict[7] = ( (1,1), (5,1), (1,7), (5,7), (1,4), (5,4), (3,2.5) ) # six, plus high middle
pip_dict[8] = ( (1,1), (5,1), (1,7), (5,7), (1,4), (5,4), (3,2.5), (3,5.5) ) # seven, plus low middle
pip_dict[9] = ( (1,1), (1,3), (1,5), (1,7), (5,1), (5,3), (5,5), (5,7), (3,4))
pip_dict[10]= ( (1,1), (1,3), (1,5), (1,7), (5,1), (5,3), (5,5), (5,7), (3,2), (3,6))

# Generate non-face cards
for suit_str in ('SPAD', 'CLUB', 'HART', 'DMND'):
    suit_img= cv2.imread(cfg[suit_str+'_IMG'])
    suit = cv2.resize(suit_img, (pip_w,pip_h))
    tius = cv2.flip(suit, 0) # flipped upside down

    for num in range(2,11):
        pips = np.zeros((pip_ny, pip_nx, 3), np.uint8)
        pips[0:pip_ny, 0:pip_nx] = hex2bgr(cfg['BACKGROUND_RGB'])
        pipxys = pip_dict[num]
        for pipx,pipy in pipxys:
            ulx = round(pipx*pip_dx - pip_dx/2)
            uly = round(pipy*pip_dy - pip_dy/2)
            if pipy < 5: # right-side up
                pips[uly:uly+pip_h, ulx:ulx+pip_w] = suit
            else:
                pips[uly:uly+pip_h, ulx:ulx+pip_w] = tius

        # TBD buffer with full print area, write in corners, buffer with bleed area
        fname = 'CARD_{}_{}.png'.format(suit_str, num)
        cv2.imwrite(fname, pips)




stophere=1




