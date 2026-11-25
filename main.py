#!/usr/bin/env python3
"""Entry program for make.fun bounty 'Sum up 24 November's world news
in one image' (news-image-20261124).

Writes one image to /output/entry.png. The image (news.png, 1024x1024,
generated locally from the day's news — see generate_image.py) is held
in this repository and simply copied, which the bounty brief explicitly
allows as the simplest valid program.

Deterministic: pure-stdlib copy, no network, no randomness, no time.
Two runs write identical bytes.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "news.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
