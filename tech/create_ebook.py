import sys
import subprocess
from pathlib import Path
import json
from html.parser import HTMLParser

def html2text(html):
  text = ''
  class MyParser(HTMLParser):
      def handle_data(self, data):
          nonlocal text
          text += data

  parser = MyParser()
  parser.feed(html)
  return text

book_dir = Path('book' if len(sys.argv) <= 1 else sys.argv[1])

meta = json.loads((book_dir / 'meta.json').read_bytes())

cover_image = book_dir / f'files/images/{meta["opf_unique_identifier_type"][1:]}.jpg'
if not cover_image.exists():
  print(f'Cover images does not exist: {cover_image}')
  sys.exit(1)

title = meta['title']
authors = [item['name'] for item in meta['authors']]

cmd = [
  'ebook-convert',
  str(book_dir / 'nav.html'),
  f'{title} - {authors[0]}.epub',
  '--title', title,
  '--authors', ' & '.join(authors),
  '--publisher', meta['publishers'][0]['name'],
  '--comments', html2text(meta['description']),
  '--cover', str(cover_image),
]
subprocess.call(cmd)
