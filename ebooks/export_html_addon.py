import re
from collections import defaultdict
from pathlib import Path
import mitmproxy.http
from mitmproxy import ctx


class ExportHtmlFiles:
  def response(self, flow: mitmproxy.http.HTTPFlow):
    """
    The full HTTP response has been read.
    """
    match = re.search(r'(\d{3,5})\.html', flow.request.path)
    if match:
      num = match.group(1)
      output_path = f'text_{num}.html'
      ctx.log.info(output_path)
      html_file = Path(output_path)
      html_file.write_bytes(flow.response.content)


addons = [
  ExportHtmlFiles()
]
