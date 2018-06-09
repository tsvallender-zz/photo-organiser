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
        sort_photo(f, split(':| ', dt))

def sort_photo(p, dt):
    year, month, day, hour, minute, second = dt
    root = Path('/home/tsv/Photos/Sorted')
    f = hour+minute+second+".jpg"
    new_path = root / year / month / day
    print(new_path)
    Path.mkdir(new_path, parents=True, exist_ok=True)
    p.rename(new_path / f)

traverse_files(Path.home() / 'Photos')

