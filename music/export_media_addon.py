import re
from collections import defaultdict
from pathlib import Path
import mitmproxy.http
from mitmproxy import ctx

class ExportMedia:
  def __init__(self):
    self.count = 0

  def response(self, flow: mitmproxy.http.HTTPFlow):
    """
    The full HTTP response has been read.
    """
    content_type = flow.response.headers.get('content-type')
    # ctx.log.info(f'{flow.request.path} | {content_type}')

    if flow.response.content is None:
      return

    if content_type == 'video/quicktime;charset=UTF-8':
      output_file = Path(f'{self.count:03}.m4a')
      output_file.write_bytes(flow.response.content)
      self.count += 1

    if flow.request.path.endswith('.jpg?param=200y200'):
      output_file = Path('cover.jpg')
      output_file.write_bytes(flow.response.content)

  def done(self):
    print(f'\nExported {self.count} audio files\n')

addons = [
  ExportMedia()
]
