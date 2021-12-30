proxy:
	python ../proxy.py

browser:
	brave -n --args --incognito --proxy-server=https://127.0.0.1:8080

export:
	mitmdump -ns export_media_addon.py -r dumpfile

assemble:
	python3 assemble_m4a_file.py

clean:
	rm *.mp4
