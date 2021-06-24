import shutil
import json
from pathlib import Path
import subprocess

book_dir = Path('book')
meta = json.loads((book_dir / 'meta.json').read_bytes())
title = meta['title']
authors = ' & '.join(item['name'] for item in meta['authors'])
output_name = f'{title} - {authors}'
output_file = f'{output_name}.tar.gz'

shutil.copy('create_ebook.py', str(book_dir))

cmd = ['tar', '-czvf', output_file, '-s', f'/^book/{output_name}/', 'book']
subprocess.call(cmd)
