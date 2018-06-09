#! /usr/bin/env python3

from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from re import split

def traverse_files(p):
    for f in p.rglob('*.jpg'):
        print(f.name)
        i = Image.open(f)
        data = i._getexif()
        for tag, value in data.items():
            if TAGS.get(tag, tag) == "DateTime":
                dt = value
                break
        print(split(':| ', dt))

traverse_files(Path.home() / 'Photos')

