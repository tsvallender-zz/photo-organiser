#! /usr/bin/env python

from PIL import Image
from PIL.ExifTags import TAGS

def get_exif(f):
    r = {}
    i = Image.open(f)
    exif = i.getexif()
    for tag, value in exif.items():
        decoded = TAGS.get(tag, tag)
        r[decoded] = value
    return r


