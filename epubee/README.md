Run

```
mitmdump -w dumpfile --anticache
```

Set your manual proxy configuration to `localhost:8080`

Go to http://cn.epubee.com/books

Read some pages.

Kill the proxy.

Run

```
mitmdump -ns export_html_addon.py -r dumpfile
```

Run

```
pipenv shell
pipenv install
python3 assemble_book.py title author
```
