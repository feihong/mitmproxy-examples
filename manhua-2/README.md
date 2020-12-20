Start proxy

    mitmdump -w dumpfile

Examine requests visually

    mitmweb -r dumpfile

Convert to sqlite database file

    mitmdump -ns to_sqlite.py -r dumpfile

Use [DB Browser for SQLite](https://sqlitebrowser.org/) to view database contents

## Analysis
