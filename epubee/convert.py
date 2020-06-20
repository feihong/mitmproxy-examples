import sys
import subprocess
import re
from pathlib import Path
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
  def __init__(self):
    super().__init__()
    self.tag = None
    self.title = None
    self.author = None
    self.done = False

  def handle_starttag(self, tag, attrs):
    self.tag = tag

  def handle_endtag(self, tag):
    if tag == 'head':
      self.done = True
    self.tag = None

  def handle_data(self, data):
    if self.tag == 'title':
      self.title = data
    elif self.tag == 'author':
      self.author = data

parser = MyHTMLParser()

with open('output.html', 'r', encoding='utf8') as fp:
  while True:
    line = fp.readline()
    parser.feed(line)
    if parser.done:
      break

file_title = parser.title.split(' / ')[0] + '.mobi'

cmd = [
  'ebook-convert',
  'output.html',
  file_title,
  '--title', parser.title,
  '--authors', parser.author,
  '--chapter', "//*[name()='h1' or name()='h2']"
]
subprocess.call(cmd)
