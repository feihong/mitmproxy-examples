import sys
import subprocess
from pathlib import Path
import json


book_dir = Path('.') if Path('meta.json').exists() else Path('book')

start_file = book_dir / 'kindle_split_003.html'
cover_image = book_dir / 'images/cover.jpg'

meta = json.loads((book_dir / 'meta.json').read_bytes())

if not cover_image.exists():
  print(f'Cover images does not exist: {cover_image}')
  sys.exit(1)

title = meta['title']
authors = ' & '.join(item['name'] for item in meta['authors'])
output_file = f'{title} - {authors}.epub'

# https://manual.calibre-ebook.com/generated/en/ebook-convert.html
cmd = [
  'ebook-convert',
  str(start_file),
  output_file,
  '--title', title,
  '--authors', authors,
  '--publisher', meta['publishers'][0]['name'],
  '--comments', meta['description'],
  '--cover', str(cover_image),
  '--isbn', meta['isbn'],
  '--pubdate', meta['issued'],
  '--tags', ', '.join(t['name'] for t in meta['topics']),
  '--level1-toc', '//h:h2',
  '--level2-toc', '//h:h3',
  '--level3-toc', '//h:h4',
  '--breadth-first',
]
subprocess.call(cmd)
