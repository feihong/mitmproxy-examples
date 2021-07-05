import json
from pathlib import Path
import sqlite3
from zipfile import ZipFile, ZIP_STORED

filename = 'dumpfile.db'
conn = sqlite3.connect(filename)
cur = conn.cursor()

output_root = Path('output')

def get_sections():
  # Use dictionary to avoid duplicate section objects
  sections = {}

  cur.execute("""
  select data from dump
  where path like '%getSectionDownloadInfo%'""")

  for row in cur.fetchall():
    obj = json.loads(row[0])
    section = obj['response']['sectionItem']

    sections[section['mangaSectionId']] = section

    print(f'{section["mangaName"]} {section["mangaSectionName"]} {section["mangaSectionTitle"]}')

  return sections.values()

sections = get_sections()

for section in sections:
  is_complete = True

  output_dir = output_root / f'{section["mangaName"]} {section["mangaSectionName"]} {section["mangaSectionTitle"]}'.strip()

  image_names = [name[1:] for name in section['mangaSectionImages']]
  for image_name in image_names:
    cur.execute(f"""
    select data from dump
    where path like '%{image_name}%';
    """)
    image_data = cur.fetchone()[0]
    if not output_dir.exists():
      output_dir.mkdir(parents=True)
    (output_dir / 'meta.json').write_text(json.dumps(section, indent=2))
    (output_dir / Path(image_name)).write_bytes(image_data)

  print(f'Wrote {len(image_names)} images to {output_dir}')

conn.close()
