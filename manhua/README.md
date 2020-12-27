## Instructions

1. Clear app cache. Go to My stuff > Settings and click Delete temporary files.
1. Start proxy

   python proxy.py

1. Set your phone to use proxy. Go to <Name of Wifi network> (i) -> Configure proxy -> Manual, enter the server and port, and hit Save.
1. Browse some episodes inside the app.
1. Convert to sqlite database file and generate cbz files

   ./process.sh

## Analysis

Examine requests visually

    mitmweb -r dumpfile

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
  - Episode id is in `data.path`, format is `/bfs/manga/{manga_id}/{episode_id}/data.index`
  - Episode id is in request POST param ep_id
  - Ignore those where `data.msg == 'Need buy episode'`
  - Paths in `data.images[].path`
- Webp images (generally larger than 100kb)
  - Path starts with `path` from `GetImageIndex` that looks like `/bfs/manga/{hash}.jpg`

SQL

You don't strictly need the `request_params` column, but not having it makes the table harder to search for
`GetImageIndex` rows since you cannot run JSON functions on blob columns like `data`.

```
CREATE TABLE dump (
  path text,
  request_params text,
  data blob
);

select * from dump
where path like path like '%GetImageIndex';

select * from dump
where path like '%ComicDetail' and request_params like '%"comic_id": "26505"%';

select * from dump
where path like '/bfs/manga/ac82935150afc0e23f39204da0ac545473458d25.jpg%';
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

1. Iterate over GetImageIndex to get episodes metadata
   1. Ignore those whose msg value is not empty
   1. Extract comid id and episode id from path
   1. Search for ComicDetail with the given comic id to get full comic and episode metadata
   1. Iterate over all image hashes to get all images
1. Generate ZIP file with title format: "{comic title} {episode title} ({number of images}).cbz"
