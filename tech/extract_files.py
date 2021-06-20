import json
from pathlib import Path
import sqlite3
import re

contents_dir = Path('./book')
images_dir = Path('./book/files/images')
images_dir.mkdir(parents=True, exist_ok=True)
styles_dir = Path('./book/files/styles')
styles_dir.mkdir(parents=True, exist_ok=True)


filename = 'dumpfile.db'
conn = sqlite3.connect(filename)
cur = conn.cursor()
html_prefix = """<html>
<body>
<style>
.programs { font-family: monospace; }
</style>
"""
html_suffix = """
</body>
</html>"""

# Extract metadata files
cur.execute("select data from dump where path like '/api/v1/book/%/'")
row = cur.fetchone()
obj = json.loads(row[0])
path = contents_dir / 'meta.json'
path.write_text(json.dumps(obj, indent=2))

# Extract textual content
cur.execute("""
select path, data from dump
where path like '/api/v1/book/%/chapter-content/xhtml/%.xhtml'
""")

for row in cur.fetchall():
  path, data = row
  path = (contents_dir / Path(path).name).with_suffix('.html')
  text = data.decode('utf8')
  # Rewrite image links
  text = re.sub(
    r'"https\:\/\/learning\.oreilly\.com\/api\/v2\/epubs\/urn\:orm\:book\:\d+\/files\/images\/(.*?\.jpg)"',
    r'"files/images/\1"',
    text,
  )
  # # Rewrite page links
  text = re.sub(
    r'"(.*?)\.xhtml(#.*)?"',
    r'"\1.html\2"',
    text,
  )
  path.write_text(html_prefix + text + html_suffix)
  print("Page:", path)

# Extract styles
# cur.execute("""
# select path, data from dump
# where path like '/api/v2/epubs/urn:orm:book:%/files/styles/%.css'
# """)

# for row in cur.fetchall():
#   path, data = row
#   path = styles_dir / Path(path).name
#   path.write_bytes(data)
#   print("Style:", path)

# Extract images
cur.execute("""
select path, data from dump
where path like '/api/v2/epubs/urn:orm:book:%/files/images/%.jpg'
""")

for row in cur.fetchall():
  path, data = row
  path = images_dir / Path(path).name
  path.write_bytes(data)
  print("Image:", path)

conn.close()
