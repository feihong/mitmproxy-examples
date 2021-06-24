import sys
import subprocess
from pathlib import Path
import json


book_dir = Path('book' if len(sys.argv) <= 1 else sys.argv[1])
meta = json.loads((book_dir / 'meta.json').read_bytes())
cover_id = meta["opf_unique_identifier_type"][1:]

cover_image = book_dir / f'files/images/{cover_id}.jpg'
if not cover_image.exists():
  print(f'Cover images does not exist: {cover_image}')
  sys.exit(1)

title = meta['title']
authors = ' & '.join(item['name'] for item in meta['authors'])
output_file = f'{title} - {authors}.epub'

cmd = [
  'ebook-convert',
  str(book_dir / 'nav.html'),
  output_file,
  '--title', title,
  '--authors', authors,
  '--publisher', meta['publishers'][0]['name'],
  '--comments', meta['description'],
  '--cover', str(cover_image),
]
subprocess.call(cmd)
