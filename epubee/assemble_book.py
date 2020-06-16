import sys
import re
from pathlib import Path
import subprocess
from io import StringIO
from lxml import etree
from pyquery import PyQuery




def get_files():
  names = list(Path('.').glob('text_*.html'))
  names.sort(key=get_file_key)
  return names


def get_file_key(file_):
  match = re.match(r'text_(\d+)\.html', str(file_))
  if match:
    return int(match.group(1))
  else:
    return None  # shouldn't happen


sio = StringIO()
sio.write("""\
<html>
  <head>
    <meta charset="utf-8" />
    <title>Book</title>
  </head>
  <body>
""")

for file_ in get_files():
  print(file_)

  doc = PyQuery(filename=file_)
  content = doc('.readercontent-inner')[0]
  content_string = etree.tostring(content, method='xml', encoding='unicode')
  sio.write(content_string + '\n\n')

sio.write("\n\n</body></html>")
output_file = Path('output.html')
output_file.write_text(sio.getvalue())
