"""
Dump flows into sqlite database so that you can randomly access them.
"""
import os.path
from pathlib import Path
from urllib.parse import parse_qs
import json
import sqlite3
import typing

import mitmproxy.http
from mitmproxy import ctx

filename = 'dumpfile.db'
create_table_statement = """
CREATE TABLE dump (
  path text,
  content_type text,
  xhash text,
  ep_id text,
  data blob
)"""

class SqliteAddon:
    def __init__(self):
      if os.path.exists(filename):
        os.remove(filename)
      self.conn = sqlite3.connect(filename)
      self.cur = self.conn.cursor()
      self.cur.execute(create_table_statement)
      self.conn.commit()

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """
        The full HTTP response has been read.
        """
        try:
          # ctx.log.info(flow.request.path)
          res = flow.response
          content_type = res.headers.get('content-type')
          if content_type:
            ep_id = ''
            try:
              request_params = parse_qs(flow.request.content.decode('utf-8'))
              ep_id = request_params['ep_id'][0]
            except:
              pass
            self.cur.execute(
              'INSERT INTO dump VALUES (?, ?, ?, ?, ?)',
              (
                flow.request.path,
                content_type,
                res.headers.get('x-hash'),
                ep_id,
                res.content,
              )
            )
        except Exception as e:
          ctx.log.error(str(e))

        self.conn.commit()

    def done(self):
        self.conn.close()
        print('\nDone!\n')

addons = [
    SqliteAddon()
]
