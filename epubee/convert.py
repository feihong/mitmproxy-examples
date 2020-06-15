import sys
import subprocess


title = sys.argv[1]
author = sys.argv[2]

cmd = [
  'ebook-convert',
  'output.html',
  title + '.mobi',
  '--title', title,
  '--authors', author,
  '--chapter', "//*[name()='h1' or name()='h2']"
]
subprocess.call(cmd)
