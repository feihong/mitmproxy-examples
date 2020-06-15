import re
import sys
from pathlib import Path
from io import StringIO


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


sio = StringIO("""\
<html>
  <head>
    <meta charset="utf-8" />
    <title>Book</title>
  </head>
  <body>
""")

for file_ in get_files():
  print(file_)

  sio.write(file_.read_text())

  output_file = Path(f'output.html')
  output_file.write_text(sio.getvalue())

sio.write("\n\n</body></html>")
