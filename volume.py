from pathlib import Path
import sys
import re
from zipfile import ZipFile, ZIP_STORED

if len(sys.argv) <= 1:
  print('Enter name of directory')
  sys.exit(0)

input_dir = Path(sys.argv[1])
if input_dir.is_file():
  print(f'{input_dir} is not a directory')
  sys.exit(0)

comic_title = None

def get_cbz_files():
  global comic_title

  # Return files sorted by name
  for file in sorted(input_dir.glob('*.cbz')):
    if re.search(r'第\w+卷', file.stem):
      continue

    title = file.stem.split(' ')[0]
    if comic_title is None:
      comic_title = title
      print(comic_title)
    else:
      assert comic_title == title, f'Comic title is {comic_title}, which does not match {title}'

    yield file

print(f'Comic title is {comic_title}\n')

# Return generator of bytes objects
def get_images(cbz_files):
  for cbz_file in cbz_files:
    print(cbz_file)
    with ZipFile(cbz_file, 'r') as zf:
      for name in sorted(zf.namelist()):
        if name.endswith('.jpg'):
          print(f'  {name}')
          yield zf.read(name)


cbz_files = list(get_cbz_files())
# Sort cbz files by modification time (st_ctime_ns doesn't work)
# cbz_files = sorted(get_cbz_files(), key=lambda p: p.stat().st_mtime_ns)
images = get_images(cbz_files)

# Write all images to big cbz file
output_file = input_dir / f'{comic_title} 第xxx卷.cbz'

with ZipFile(output_file, 'w') as zf:
  for i, data in enumerate(images, 1):
    zf.writestr(f'{i:03}.jpg', data, compress_type=ZIP_STORED)

  print(f'\nWrote {i} images to {output_file}')
