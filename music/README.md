# Music

1. `make proxy`
1. `make browser`
1. https://music.163.com/song?id=1818353205
1. Play song
1. Copy metadata into `meta.txt`
1. Wait for song to finish playing
1. Kill the proxy
1. (Optional) Examine requests visually `mitmweb -r dumpfile`
1. `make export`
1. Rename the main m4a file to `input.m4a`
1. `make assemble`

## Notes

Lyrics are also available at https://music.163.com/weapi/song/lyric?csrf_token=, although it's pretty easy to just copy and paste them.

After you click Play, it takes a long time for the song to start playing. Streaming doesn't work like it does in Chrome. Either mitmproxy, Brave, or the combination thereof causes the audio file to be downloaded in one big chunk instead of many small chunks.
