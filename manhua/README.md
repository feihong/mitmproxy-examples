Start proxy

    mitmdump -w dumpfile

Examine requests visually

    mitmweb -r dumpfile

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
  request_body text,
  data blob
)
```

Data structure

```javascript
comic: {
  title: s,
  episodes: [
    {
      id: i,
      title: s,
      images: [list_of_xhash]
    }
  ]
]
```
