#!/usr/bin/env python3

import sys
import os
import yt_dlp
import ffmpeg
import urllib.request
import shutil
import subprocess

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
    thumb = info.get("thumbnail")
    urllib.request.urlretrieve(thumb, "ytdl_cover.jpg")
    ydl.process_info(info)

filename_opus = filename[:-5] + ".opus"
ffmpeg.input(filename).output(filename_opus).run()
os.unlink(filename)

if shutil.which("opustags"):
    subprocess.run(["opustags", "--set-cover", "ytdl_cover.jpg", filename_opus, "-i"])
os.unlink("ytdl_cover.jpg")
