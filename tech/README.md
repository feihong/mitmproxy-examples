## Instructions

1. Start proxy
   ```
   python proxy.py
   ```
1. Set your phone to use proxy. Go to "Name of Wifi network ℹ️" -> Configure proxy -> Manual, enter the server and port, and hit Save.
1. Download book
1. Convert to sqlite database file
   ```
   mitmdump -ns to_sqlite.py -r dumpfile
   ```
1. Extract files from sqlite database
   ```
   python extract_files.py
   ```

## Analysis

Examine requests visually

    mitmweb -r dumpfile

Use [DB Browser for SQLite](https://sqlitebrowser.org/) to view database contents

## Analysis

- /api/v1/book/<book_id>/
  - Full metadata in JSON
  - source already has value "application/epub+zip"
  - title
  - orderable_author
  - description
  - pagecount
  - chapters
    - Links to all chapter .xhtml files
- /api/v1/book/<book_id>/chapter-content/xhtml/contents.xhtml
  - Content
- /api/v2/epubs/urn:orm:book:<book_id>/files/images/<file_name>.jpg
  - Image asset
- /api/v2/epubs/urn:orm:book:<book_id>/files/styles/<file_name>.css
  - CSS asset

## Algorithm
