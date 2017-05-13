#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from PIL import Image
import imagehash, os

import imagehash

hashfuncs = [imagehash.average_hash, imagehash.phash, imagehash.dhash, imagehash.whash]

verbose = True

"""
Demo of hashing
"""
def find_similar_images(userpath):
    imghashes = [{} for i in hashfuncs]
    imgfiles = {}
    try:
        with open("hashes.txt","r") as f:
            for line in f:
                hl = line.rstrip("\n").split("\t")
                if len(hl) < len(hashfuncs)+1:
                    continue
                if not hl[0].startswith(userpath):
                    continue
                if not os.path.isfile(hl[0]):
                    continue
                imgfiles[hl[0]] = hl[1:]
                for i in range(len(hashfuncs)):
                    imghashes[i][hl[i+1]] = imghashes[i].get(hl[i+1],[]) + [hl[0]]
    except:
        pass
    hashfile = open("hashes.txt","a")

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
    for img in image_filenames:
        if img in imgfiles:
            continue
        if verbose:
            print(img)
        hl = []
        for i in range(len(hashfuncs)):
            hash = str(hashfuncs[i](Image.open(img)))
            hl += [hash]
            imghashes[i][hash] = imghashes[i].get(hash, []) + [img]
        imgfiles[img] = hl
        hashfile.write(img + "\t" + "\t".join(hl) + "\n")
        hashfile.flush()

    while len(imgfiles) > 0:
        img, hashes = imgfiles.popitem()
        imgs = {img: True}
        for i in range(len(hashfuncs)):
            for nimg in imghashes[i][hashes[i]]:
                imgs[nimg] = True
                imgfiles.pop(nimg, None)
        if len(imgs) > 1:
            print("\t".join(imgs.keys()))


if __name__ == '__main__':
    import sys
    def usage():
        sys.stderr.write("""SYNOPSIS: %s [<directory>]

Identifies similar images in the directory.

(C) Johannes Buchner, 2013-2017
(C) Michael Vigovsky, 2017
""" % sys.argv[0])
        sys.exit(1)

    userpath = sys.argv[1] if len(sys.argv) > 1 else "."
    find_similar_images(userpath=userpath)
