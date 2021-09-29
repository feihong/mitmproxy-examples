import enum
import json
import re
import sqlite3
from zipfile import ZipFile, ZIP_STORED

filename = 'dumpfile.db'
conn = sqlite3.connect(filename)
cur = conn.cursor()

manga_title = None
cur.execute("select path, data from dump where path like '/manga/%';")
for (path, data) in cur.fetchall():
  if 'feed' in path:
    continue
  manga = json.loads(data)
  try:
    manga_title = manga['data']['attributes']['title']['en']
  except:
    pass

print(manga_title)

chapters = []
cur.execute("select data from dump where path like '/chapter/%';")
for (data,) in cur.fetchall():
  chapter = json.loads(data)['data']['attributes']
  chapters.append(chapter)

for chapter in chapters:
  # print(chapter['chapter'])

  image_filenames = chapter['data']
  images = []
  for image in image_filenames:
    cur.execute(f"select data from dump where path like '/data/%/{image}'")
    data = None
    for (blob,) in cur.fetchall():
      if blob is not None:
        data = blob

    if data is None:
      print(f'Missing image: {image}')
    else:
      images.append(data)

    warning = ''
    if len(images) < len(image_filenames):
      warning = f", should be {len(image_filenames)}"

    title = f'{manga_title} Ch {chapter["chapter"]}'
    output_file = f'{title} ({len(images)}{warning}).cbz'

  with ZipFile(output_file, 'w') as zf:
    for i, data in enumerate(images, 1):
      image_file = f'{i:03}.jpg'
      zf.writestr(image_file, data, compress_type=ZIP_STORED)

  print(f'Wrote {len(images)} images to {output_file}')

conn.close()
