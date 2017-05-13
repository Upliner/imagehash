#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from PIL import Image
import six, imagehash, os

import imagehash

verbose = True
"""
Demo of hashing
"""
def find_similar_images(userpath, hashfunc = imagehash.average_hash):

    def is_image(filename):
        f = filename.lower()
        return f.endswith(".png") or f.endswith(".jpg") or \
            f.endswith(".jpeg") or f.endswith(".bmp") or f.endswith(".gif")

    def walk(path):
        for tup in os.walk(path):
            for f in tup[2]:
                if is_image(f):
                    yield tup[0]+"/"+f

    image_filenames = walk(userpath)
    images = {}
    for img in image_filenames:
        hash = hashfunc(Image.open(img))
        if verbose:
             print(img + " " + str(hash))
        images[hash] = images.get(hash, []) + [img]

    for k, img_list in six.iteritems(images):
        if len(img_list) > 1:
            print(" ".join(img_list))


if __name__ == '__main__':
    import sys
    def usage():
        sys.stderr.write("""SYNOPSIS: %s [ahash|phash|dhash|...] [<directory>]

Identifies similar images in the directory.

Method: 
  ahash:      Average hash
  phash:      Perceptual hash
  dhash:      Difference hash
  whash-haar: Haar wavelet hash
  whash-db4:  Daubechies wavelet hash

(C) Johannes Buchner, 2013-2017
""" % sys.argv[0])
        sys.exit(1)

    hashmethod = sys.argv[1] if len(sys.argv) > 1 else usage()
    if hashmethod == 'ahash':
        hashfunc = imagehash.average_hash
    elif hashmethod == 'phash':
        hashfunc = imagehash.phash
    elif hashmethod == 'dhash':
        hashfunc = imagehash.dhash
    elif hashmethod == 'whash-haar':
        hashfunc = imagehash.whash
    elif hashmethod == 'whash-db4':
        hashfunc = lambda img: imagehash.whash(img, mode='db4')
    else:
        usage()
    userpath = sys.argv[2] if len(sys.argv) > 2 else "."
    find_similar_images(userpath=userpath, hashfunc=hashfunc)
