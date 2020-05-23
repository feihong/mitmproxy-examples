Run

```
mitmdump -w dumpfile --anticache
```

Set your manual proxy configuration to `localhost:8080`

Go to https://soundcloud.com/noamhassenfeld/sets/todayexplained

Play some songs.

Kill the proxy.

Run

```
mitmdump -ns export_mp3_addon.py -r dumpfile
```

Run

```
python3 assemble_mp3_files.py
```
