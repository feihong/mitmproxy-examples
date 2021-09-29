"""
Dump flows into sqlite database so that you can randomly access them.
"""
import os.path
from pathlib import Path
from urllib.parse import parse_qsl
import json
import sqlite3
import typing

import mitmproxy.http
from mitmproxy import ctx

filename = 'dumpfile.db'
create_table_statement = """
CREATE TABLE dump (
  path text,
  request_params text,
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
          req = flow.request
          res = flow.response
          request_params = None
          if req.headers.get('content-type') == 'application/x-www-form-urlencoded':
            try:
              request_params = json.dumps(dict(parse_qsl(flow.request.content.decode('utf-8'))))
            except:
              pass
          self.cur.execute(
            'INSERT INTO dump VALUES (?, ?, ?)',
            (
              flow.request.path,
              request_params,
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
