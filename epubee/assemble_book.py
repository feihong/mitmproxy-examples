import sys
import re
from pathlib import Path
import subprocess
from io import StringIO
from lxml import etree
from pyquery import pyquery


title = sys.argv[1]
author = sys.argv[2]


def get_files():
  names = list(Path('.').glob('text_*.html'))
  names.sort(key=get_file_key)
  return names


def get_file_key(file_):
  match = re.match(r'.+text_(\d+).mp3', str(file_))
  if match:
    return int(match.group(1))
  else:
    return None  # shouldn't happen


sio = StringIO(f"""\
<html>
  <head>
    <meta charset="utf-8" />
    <title>{title} - {author}</title>
  </head>
  <body>
""")

for file_ in get_files():
  print(file_)

  doc = PyQuery(filename=file_)
  content = doc('.readercontent-inner')[0]
  sio.write(etree.tostring(content) + '\n\n')

  # sio.write(file_.read_text())

sio.write("\n\n</body></html>")
output_file = Path('output.html')
output_file.write_text(sio.getvalue())

# cmd = [
#   'ebook-convert',
#   'output.html',
#   title + '.mobi',
#   '--title', title,
#   '--authors', author,
#   '--chapter', "//*[name()='h1' or name()='h2']"
# ]
# subprocess.call(cmd)
