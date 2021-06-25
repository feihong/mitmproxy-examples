import json
from pathlib import Path
import sqlite3
import re


contents_dir = Path('./book')
images_dir = Path('./book/images')
images_dir.mkdir(parents=True, exist_ok=True)

filename = 'dumpfile.db'
conn = sqlite3.connect(filename)
cur = conn.cursor()
html_prefix = """<html>
<body>
"""
html_suffix = """
</body>
</html>"""

# Extract metadata and toc files
cur.execute("select path, data from dump where path like '/api/v1/book/%/'")
meta = None
for row in cur.fetchall():
  path, data = row
  if re.match(r'^/api/v1/book/\d+/$', path):
    try:
      meta = json.loads(data)
    except:
      pass

path = contents_dir / 'meta.json'
path.write_text(json.dumps(meta, indent=2))

book_id = meta['identifier']
print(f'Title: {meta["title"]}, Id: {book_id}')

cur.execute(f"select path, data from dump where path = '/api/v1/book/{book_id}/toc/'")
_, data = cur.fetchone()
toc = json.loads(data)
path = contents_dir / 'toc.json'
path.write_text(json.dumps(toc, indent=2))

# Extract textual content
cur.execute(f"""
select path, data from dump
where path like '/api/v1/book/{book_id}/chapter-content/%'
""")

for row in cur.fetchall():
  path, data = row
  path = (contents_dir / Path(path).name).with_suffix('.html')  # in case of .xhtml file
  text = data.decode('utf8')
  # Rewrite image links
  text = re.sub(
    r'"https\:\/\/learning\.oreilly\.com\/api\/v2\/epubs\/urn\:orm\:book\:\d+\/files\/(.*?\.jpg)"',
    r'"images/\1"',
    text,
  )
  # Rewrite page links
  text = re.sub(
    r'"(.*?)\.xhtml(#.*)?"',
    r'"\1.html\2"',
    text,
  )
  path.write_text(html_prefix + text + html_suffix)
  print("Page:", path)

# Extract images
cur.execute(f"""
select path, data from dump
where path like '/api/v2/epubs/urn:orm:book:{book_id}/files/%.jpg'
""")

for row in cur.fetchall():
  path, data = row
  path = images_dir / Path(path).name
  path.write_bytes(data)
  print("Image:", path)

conn.close()
