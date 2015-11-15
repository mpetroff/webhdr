#!/usr/bin/env python

'''
Convert high dynamic range image into WebHDR
Matthew Petroff <https://mpetroff.net>, November 2015

This script is released into the public domain using the CC0 1.0 Public
Domain Dedication: https://creativecommons.org/publicdomain/zero/1.0/

The method implemented is based on:
Francesco Banterle and Roberto Scopigno. BoostHDR: a novel backward-
compatible method for HDR images. 2012. DOI: 10.1117/12.931504. URL:
http://vcg.isti.cnr.it/Publications/2012/BS12/spie_2012_compression_hdr.pdf
'''

import argparse
import numpy as np
import imageio

# Parse arguments
parser = argparse.ArgumentParser(description='Convert image to WebHDR.')
parser.add_argument('file', metavar='FILE', type=str,
                    help='Image file to convert (e.g. image.exr)')
args = parser.parse_args()

# Load image
image = np.array(imageio.imread(args.file))

# Create compression-driven map
L = 0.213 * image[..., 0] + 0.715 * image[..., 1] + 0.072 * image[..., 2]
Llog = np.log10(L)
Lfloor = np.floor(Llog).astype(np.int8)
done = False
while not done:
    done = True
    prev_lmean = -np.inf
    prev_i = np.iinfo(np.int32).min
    for i in np.unique(Lfloor):
        lmean = np.average(Llog, weights=(Lfloor == i))
        if lmean - prev_lmean < 1:
            Lfloor = np.where(Lfloor == i, np.ones_like(Lfloor) * prev_i, Lfloor)
            done = False
            break
        prev_lmean = lmean
        prev_i = i

# Tone map
Ld = np.empty_like(image)
cdm = np.empty_like(L).astype(np.uint8)
imglog = np.log10(image)
for i in np.unique(Lfloor):
    lmean = np.average(Llog, weights=(Lfloor == i))
    a = np.clip(lmean / 4, -8, 8)
    a = int((a + 8) * 16)
    cdm = np.where(Lfloor == i, a, cdm)
    a = float(a) / 16 - 8
    Ld = np.where(np.expand_dims(Lfloor, 2) == i, (a * imglog) / (a * imglog + 1), Ld)
Ld = np.clip(Ld, 0, 1)

# Convert to images and save
imageio.imsave(args.file.split('.')[0] + '_ld.jpg', Ld, quality=90,
               progressive=True, optimize=True, baseline=True)
imageio.imsave(args.file.split('.')[0] + '_cdm.png', cdm)
