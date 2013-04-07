#!/usr/bin/env python
import socket
import sys
import tempfile
from SimpleCV import *


def get_image(filename="tmp.jpg"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.0.106", 8081))

    fh = s.makefile()
# Read in HTTP headers:
    line = fh.readline()
    boundary = ""
    while line.strip() != '':
        parts = line.split(':')
        if len(parts) > 1 and parts[0].lower() == 'content-type':
            # Extract boundary string from content-type
            content_type = parts[1].strip()
            boundary = content_type.split(';')[1].split('=')[1]
        line = fh.readline()

    if not boundary:
        raise Exception("Can't find content-type")

# Seek ahead to the first chunk
    while line.strip() != boundary:
        line = fh.readline()

# Read in chunk headers
    while line.strip() != '':
        parts = line.split(':')
        if len(parts) > 1 and parts[0].lower() == 'content-length':
            # Grab chunk length
            length = int(parts[1].strip())
        line = fh.readline()

    image = fh.read(length)
    t = open(filename,"w")
    t.write(image)
    t.close()
    return filename
