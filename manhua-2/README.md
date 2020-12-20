Start proxy

    mitmdump -w dumpfile

Examine requests visually

    mitmweb -r dumpfile

Convert to sqlite database file

    mitmdump -ns to_sqlite.py -r dumpfile

Use [DB Browser for SQLite](https://sqlitebrowser.org/) to view database contents

## Analysis

Key requests

- getSectionDownloadInfo
  - response
    - sectionItem
      - mangaSectionId
      - mangaName
      - mangaSectionName
      - mangeSectionTitle
      - mangaSectionImages
        - Just file names, e.g. `/1_2896.jpg`
- `{page_number}_{image_id}.jpg?cid={manga_section_id}`
  - Example: `1_2896.jpg?cid=156436`
  - `cid` matches `mangaSectionId`

SQL table

```
CREATE TABLE dump (
  path text,
  data blob
)
```

Data structures

```
sections: {
  [id]: {
    comicTitle: s,
    title: s,
    images: [fileName],
    complete: t,
  }
}
```

Algorithm

1. Iterate over getSectionDownloadInfo to build map of section metadata
   1. Iterate over image file requests to get all images
1. Generate ZIP file with title format: "{comic title} {episode title} ({number of images}).cbz"
