import re
import sys
from pathlib import Path


def get_filenames():
  names = set()

  for p in Path('.').glob('*.mp3'):
    match = re.match(r'(.*)_\d+\.mp3', str(p))
    if match:
      names.add(match.group(1))

  return names

def get_file_key(file_):
  match = re.match(r'.+_(\d+).mp3', str(file_))
  if match:
    return int(match.group(1))
  else:
    return None  # shouldn't happen

for name in get_filenames():
  print(name)
  buf = bytearray()

  files = Path('.').glob(f'{name}_*.mp3')
  for file_ in sorted(files, key=get_file_key):
    buf.extend(file_.read_bytes())

  output_file = Path(f'{name}.mp3')
  output_file.write_bytes(buf)

