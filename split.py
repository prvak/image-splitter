#!/usr/bin/python
from reportlab.pdfgen import canvas
from PIL import *
import argparse
import os
import math

def split(img, cols, rows):
    """Split image into cols*rows regions. Returns regions as generator."""
    (width, height) = img.size
    w = width/cols
    h = height/rows
    coordinates = ((x, y)
            for x in range(cols)
            for y in range(rows))
    return (img.crop((x*w, y*h, x*w+w, y*h+h)) for x, y in coordinates)

verbose = False
def log(message):
    if (verbose):
        print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Split image to several smaler images.")
    parser.add_argument("-r", "--rows", type = int, default = 2,
            help = "how many rows to create")
    parser.add_argument("-c", "--cols", type = int, default = 2,
            help="how many columns to create")
    parser.add_argument("-v", "--verbose", action = "store_true",
            help="if not specified, the program will not output anything")
    parser.add_argument("image", type = str, 
            help="path to the image")
    args = parser.parse_args()
    
    # Set output verbosity.
    verbose = args.verbose

    # Split the image into subimages.
    log("Splitting image '%s'." % args.image)
    img = Image.open(args.image)
    regions = split(img, args.cols, args.rows);
    
    # Construct template filename.
    root, ext = os.path.splitext(args.image)
    precision = int(math.ceil(math.log(args.rows * args.cols, 10)))
    pathTemplate = "%s-%%0%dd.png" % (root, precision) #eg. image-%02d.png

    # Save subimages.
    for i, region in enumerate(regions):
        path = pathTemplate % (i)
        log("Generating subimage '%s'." % path)
        region.save(path)

    log("Done.")
