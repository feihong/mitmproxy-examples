import re
from collections import defaultdict
from pathlib import Path
import mitmproxy.http
from mitmproxy import ctx

class ExportMp3Files:
  def __init__(self):
    self.counts = defaultdict(int)

  def response(self, flow: mitmproxy.http.HTTPFlow):
    """
    The full HTTP response has been read.
    """
    content_type = flow.response.headers.get('content-type')
    # ctx.log.info(flow.request.path + ' | ' + content_type)

    if content_type == 'audio/mpeg':
      match = re.search(r'\/([a-zA-Z0-9]+)\.128\.mp3', flow.request.path)
      if match:
        name = match.group(1)
        output_path = f'{name}_{self.counts[name]}.mp3'
        ctx.log.info(output_path)
        mp3_file = Path(output_path)
        mp3_file.write_bytes(flow.response.content)

        self.counts[name] += 1

addons = [
  ExportMp3Files()
]
