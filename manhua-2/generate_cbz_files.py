import json
from pathlib import Path
import subprocess
from zipfile import ZipFile, ZIP_STORED

input_root = Path('output')

def split_image(image, image_file):
  left_file = image_file.with_name(image_file.stem + '_l' + image_file.suffix)
  right_file = image_file.with_name(image_file.stem + '_r' + image_file.suffix)
  w = image['width']
  h = image['height']

  subprocess.call([
    'magick', 'convert', str(image_file), '-crop',
    f'{w / 2}x{h}+0+0',
    str(left_file),
  ])
  subprocess.call([
    'magick', 'convert', str(image_file), '-crop',
    f'{w / 2}x{h}+{w / 2}+0',
    str(right_file),
  ])
  return left_file, right_file


for input_dir in input_root.iterdir():
  if not input_dir.is_dir():
    continue

  output_file = input_dir.name + '.cbz'

  meta = json.loads(Path(input_dir / 'meta.json').read_bytes())

  def get_images():
    for (name, item) in zip(meta['mangaSectionImages'], meta['inciseInfo']):
      item['name'] = name[1:]
      yield item

  images = list(get_images())

  with ZipFile(output_file, 'w') as zf:
    count = 1
    for image in images:
      image_file = input_dir / image['name']
      print(image_file)

      if image['pageType'] == 0:
        # ZIP_STORED means no compression
        zf.writestr(f'{count:03}.jpg', image_file.read_bytes(), compress_type=ZIP_STORED)
        count += 1
      elif image['pageType'] == 1:
        # Cut into 2 pages
        left_file, right_file = split_image(image, image_file)
        zf.writestr(f'{count:03}.jpg', right_file.read_bytes(), compress_type=ZIP_STORED)
        zf.writestr(f'{count + 1:03}.jpg', left_file.read_bytes(), compress_type=ZIP_STORED)
        count += 2

  print(f'Wrote {len(images)} images to {output_file}')
