"""
Add album art and adjust gain
"""
from pathlib import Path
import subprocess
import shutil
import mutagen.mp4
from mutagen.mp4 import MP4Cover

input_file = Path('input.m4a')
image_file = Path('cover.jpg')
meta_file = Path('meta.txt')

lines = meta_file.read_text().splitlines()
title, artist, *rest = lines
lyrics = '\n'.join(rest)

output_file = Path(f'{artist}  {title}.m4a')

shutil.copy(input_file, output_file)

mp4 = mutagen.mp4.MP4(output_file)
mp4['©nam'] = title
mp4['©ART'] = artist
mp4['©lyr'] = lyrics
mp4['covr'] = [MP4Cover(image_file.read_bytes(), imageformat=MP4Cover.FORMAT_JPEG)]
mp4.save()

subprocess.run([
  'aacgain',
  "-r", # apply Track gain automatically (all files set to equal loudness)
  "-k", # automatically lower Track/Album gain to not clip audio
  output_file,
])
