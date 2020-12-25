import json
import re
import sqlite3
from zipfile import ZipFile, ZIP_STORED

filename = 'dumpfile.db'
conn = sqlite3.connect(filename)
cur = conn.cursor()

cur.execute("""
select data from dump
where path like '%GetImageIndex';
""")

comics = {}
episodes = []

for row in cur.fetchall():
  obj = json.loads(row[0])
  episode = obj['data']
  path = episode['path']
  if not path: continue
  match = re.match(r"/bfs/manga/(\d+)/(\d+)", episode['path'])
  comic_id = match.group(1)
  episode['comic_id'] = comic_id
  episode['id'] = int(match.group(2))
  episodes.append(episode)

  # print(f'{episode["comic_id"]} {episode["id"]}')

  comic = comics.get(comic_id)
  if comic is None:
    cur.execute(f"""
    select data from dump
    where path like '%ComicDetail' and request_params like '%"comic_id": "{comic_id}"%';
    """)
    comic = json.loads(cur.fetchone()[0])['data']
    comic[comic_id] = comic

  episode_detail = [ep for ep in comic['ep_list'] if ep['id'] == episode['id']][0]
  episode['detail'] = episode_detail

  # print(f'{comic["title"]} {episode_detail["title"]}')

  is_complete = True
  images = []
  for image in episode['images']:
    cur.execute(f"""
    select data from dump
    where path like '{image["path"]}%';
    """)
    try:
      images.append(cur.fetchone()[0])
    except:
      is_complete = False

  output_file = f'{comic["title"]} {episode_detail["title"]}{"" if is_complete else " (NOT COMPLETE)"}.cbz'
  with ZipFile(output_file, 'w') as zf:
    for i, data in enumerate(images, 1):
      zf.writestr(f'{i:03}.jpg', data, compress_type=ZIP_STORED)

  print(f'Wrote {len(images)} images to {output_file}')

conn.close()
