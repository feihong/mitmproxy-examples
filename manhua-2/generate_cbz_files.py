import json
import sqlite3
from zipfile import ZipFile, ZIP_STORED

filename = 'dumpfile.db'
conn = sqlite3.connect(filename)
cur = conn.cursor()

cur.execute("""
select data from dump
where path like '%getSectionDownloadInfo%'""")

sections = []

for row in cur.fetchall():
  obj = json.loads(row[0])
  section = obj['response']['sectionItem']
  sections.append(section)

  print(f'{section["mangaName"]} {section["mangaSectionName"]} {section["mangaSectionTitle"]}')

for section in sections:
  is_complete = True

  output_file = f'{section["mangaName"]} {section["mangaSectionName"]} {section["mangaSectionTitle"]}'.strip() + '.cbz'

  images = []   # list of bytes
  for image_path in section['mangaSectionImages']:
    cur.execute(f"""
    select data from dump
    where path like '%{image_path}%';
    """)
    images.append(cur.fetchone()[0])

  with ZipFile(output_file, 'w') as zf:
    for i, data in enumerate(images, 1):
      zf.writestr(f'{i:03}.jpg', data, compress_type=ZIP_STORED)

  print(f'Wrote {len(images)} images to {output_file}')

conn.close()
