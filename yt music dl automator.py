#!/usr/bin/env python3

import sys
import os
import yt_dlp
import ffmpeg

if len(sys.argv) < 2:
    print("Enter a youtube URL to download")
    sys.exit(1)

mypath = os.path.abspath(".")
yturl = sys.argv[1]
filename = ""

ydl_opts = {"format": "251", "outtmpl": "%(title)s.%(ext)s"}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(yturl, download=False)
    filename = ydl.prepare_filename(info)
    ydl.process_info(info)

filename_opus = filename[:-5] + ".opus"
ffmpeg.input(filename).output(filename_opus).run()
