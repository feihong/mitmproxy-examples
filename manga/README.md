## Instructions

1. Clear app cache. Go to My stuff > Settings and click Delete temporary files.
1. Start proxy
   ```
   make proxy
   ```
1. Set your phone to use proxy. Go to "Name of Wifi network ℹ️" -> Configure proxy -> Manual, enter the server and port, and hit Save.
1. Browse some episodes inside the app. You can also try downloading entire episodes, but it might be best to download episodes one at a time rather than in a batch.
1. Convert to sqlite database file, then generate CBZ files
   ```
   make process
   ```
1. Consolidate CBZ files into a single volume file
   ```
   make volume
   ```

### Inspect

1. Examine requests visually
   ```
   mitmweb -r dumpfile
   ```
1. Use [DB Browser for SQLite](https://sqlitebrowser.org/) to view database contents

## Analysis

- Series detail
  - Example: /manga/a6755221-23ba-4ad2-b98f-b852387375bb?includes[]=artist&includes[]=author&includes[]=cover_art
  - Title in `data.attributes.title.en`
- Multiple chapter detail (ignore)
  - Example: /manga/a6755221-23ba-4ad2-b98f-b852387375bb/feed?limit=96&includes[]=scanlation_group&includes[]=user&order[volume]=desc&order[chapter]=desc&offset=0&contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&contentRating[]=pornographic
  - Chapter objects in `data`
  - Chapter number in `data[n].attributes.chapter`
  - Chapter images in `data[n].attributes.data`
- Single chapter detail
  - Example: /chapter/6d835bf8-02fc-4de9-8d97-104f901f327b?includes[]=scanlation_group&includes[]=manga&includes[]=user
  - Chapter number in `data.attributes.chapter`
  - Chapter images in `data.attributes.data`
- Image
  - Example: /data/64a31a476615edbaac5eb526efee07fd/z2-8445e154a928c2c257e3ab8dd506f0a7a871b03440d0576dd082706d0300c6d6.jpg

## SQL

```
CREATE TABLE dump (
  path text,
  request_params text,
  data blob
);

select * from dump
where path like path like '/manga/%';

select * from dump
where path like '/chapter/%';

select * from dump
where path like '/data/%/z2-8445e154a928c2c257e3ab8dd506f0a7a871b03440d0576dd082706d0300c6d6.jpg';
```

## Algorithm

1. Retrieve latest series detail
1. Retrieve all single chapter details
   1. Iterate over all image file names to get images
1. Generate ZIP file with title format: "{series title} {chapter number} ({number of images}).cbz"
