import json
import re
import sqlite3
from zipfile import ZipFile, ZIP_STORED

filename = 'dumpfile.db'
conn = sqlite3.connect(filename)
cur = conn.cursor()

def get_comics():
  comics = {}
  cur.execute("select data from dump where path like '%ComicDetail%';")
  for row in cur.fetchall():
    comic = json.loads(row[0])['data']
    comic_id = str(comic['id'])
    comics[comic_id] = comic

  return comics

comics = get_comics()

def get_episodes():
  episodes = {}
  cur.execute("select data from dump where path like '%GetImageIndex%';")

  for row in cur.fetchall():
    episode = json.loads(row[0])['data']
    path = episode['path']
    if not path: continue
    match = re.match(r"/bfs/manga/(\d+)/(\d+)", episode['path'])
    comic_id = match.group(1)
    episode['comic'] = comics[comic_id]
    episode_id = int(match.group(2))
    episode['id'] = episode_id
    episodes[episode_id] = episode
    print(f'{comic_id} {episode_id}')

  return episodes.values()

episodes = get_episodes()

for episode in episodes:
  comic = episode['comic']

  try:
    detail = [ep for ep in comic['ep_list'] if ep['id'] == episode['id']][0]
  except IndexError:
    print(f'Could not find details for episode {episode["id"]}')
    continue

  episode['detail'] = detail

  chapter = f'{comic["title"]} {detail["title"]}'

  is_complete = True
  images = []
  for image in episode['images']:
    cur.execute(f"""
    select data from dump
    where path like '{image["path"]}%';
    """)
    try:
      data = None
      for (blob,) in cur.fetchall():
        if blob is not None:
          data = blob
      if data is None:
        print(f'No data found for {chapter} {image["path"]}')
      else:
        images.append(data)
    except:
      is_complete = False

  warning = ''
  if len(images) < len(episode['images']):
    warning = f", should be {len(episode['images'])}"

  title = ' '.join(s.strip() for s in [comic['title'], detail['short_title'], detail['title']] if s.strip())
  output_file = f"{title} ({len(images)}{warning}).cbz"

  with ZipFile(output_file, 'w') as zf:
    for i, data in enumerate(images, 1):
      image_file = f'{i:03}.jpg'
      zf.writestr(image_file, data, compress_type=ZIP_STORED)

  print(f'Wrote {len(images)} images to {output_file}')

conn.close()
