Start proxy

    mitmdump -w dumpfile

Examine requests visually

    mitmweb -r dumpfile

Convert to sqlite database file

    mitmdump -ns to_sqlite.py -r dumpfile

Use [DB Browser for SQLite](https://sqlitebrowser.org/) to view database contents

## Analysis

- ComicDetail
  - Comic title in `data.title`
  - Episode/chapter metadata in `data.ep_list[]`
    - Episode title in `title`
    - Episode id in `id`
- GetEpisodeLikeState
  - Always requested when user starts reading new chapter
- GetImageIndex
  - Tells you order images come in as well as their size
  - Episode id is in request POST param ep_id
  - Ignore those where `data.msg == 'Need buy episode'`
  - Paths in `data.images[].path`
- Webp images (generally larger than 100kb)
  - Header `X-Hash` set to `path` from `GetImageIndex` that looks like `/bfs/manga/{hash}.jpg`

SQL table

```
CREATE TABLE dump (
  path text,
  content_type text,
  xhash text,
  ep_id text,
  data blob
)
```

Data structures

```
episodes: {
  [id]: {
    comicTitle: s,
    title: s,
    images: [xhash],
    complete: t,
  }
}

episode: {
  id: i,
  images: [xhash],
}
```

Algorithm

1. Iterate over ComicDetail to build map of episode metadata
1. Iterate over GetImageIndex to get all episodes and their respective image hashes
   1. Iterate over all image hashes to get all images
1. Generate ZIP file with title format: "{comic title} {episode title} ({number of images}).cbz"
