#! /usr/bin/env python3

import argparse
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from re import split
import shutil

def main():
    parser = argparse.ArgumentParser(description="Sort photos by date.")
    parser.add_argument('-i', '--input',
                        help="Input folder")
    parser.add_argument('-o', '--output',
                        help="Output folder")
    parser.add_argument('-d', '--duplicates',
                        help="Detect and delete duplicates",
                        action="store_true")
    parser.add_argument('-f', '--folder',
                        help="Folder structure for output")
    parser.add_argument('-v', '--verbose',
                        help="Verbose mode",
                        action="store_true")
    parser.add_argument('-n', '--noaction',
                        help="Don't perform any action",
                        action="store_true")
    parser.add_argument('-r', "--remove",
                        help="Delete original file",
                        action="store_true")
    args = parser.parse_args()
    photosort = PhotoSort(args)
    photosort.run()

class PhotoSort(object):
    def __init__(self, flags):
        self.flags = flags

    def run(self):
        if self.flags.input:
            self.traverse_files(Path(self.flags.input))
        else:
            print("No input specified")
            exit

    def traverse_files(self, p):
        for f in p.rglob('*.jpg'):
            i = Image.open(f)
            data = i._getexif()
            for tag, value in data.items():
                if TAGS.get(tag, tag) == "DateTime":
                    dt = value
                    break
            self.sort_photo(f, split(':| ', dt))

    def sort_photo(self, p, dt):
        year, month, day, hour, minute, second = dt

        if self.flags.output:
            # This needs to be checked
            new_path = Path(self.flags.output)
        else:
            new_path = Path.home()
        new_path = new_path / year / month / day

        f = hour+minute+second+".jpg"

        if self.flags.verbose:
            print("Moving to image to " + str(new_path) + '/' + f)
        if not self.flags.noaction:
            Path.mkdir(new_path, parents=True, exist_ok=True)
            if self.flags.remove:
                p.rename(new_path / f)
            else:
                shutil.copyfile(str(p), str(new_path) +'/' + f) 
                
if __name__ == "__main__":
    main()

