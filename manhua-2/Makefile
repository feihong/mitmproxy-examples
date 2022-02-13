proxy:
	python ../proxy.py

process: db cbz

db:
	mitmdump -ns ../to_sqlite.py -r dumpfile

files:
	python extract_files.py

cbz:
	python generate_cbz_files.py

volume:
	python ../volume.py .

clean:
	rm dumpfile && rm dumpfile.db
