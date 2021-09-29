proxy:
	pipenv run python ../proxy.py

process: db cbz

db:
	pipenv run mitmdump -ns ../to_sqlite.py -r dumpfile

cbz:
	pipenv run python generate_cbz_files.py

volume:
	pipenv run python ../volume.py .

clean:
	rm dumpfile && rm dumpfile.db
