proxy:
	pipenv run python ../proxy.py

db:
	pipenv run mitmdump -ns to_sqlite.py -r dumpfile

cbz:
	pipenv run python generate_cbz_files.py

volume:
	echo "not implemented"

clean:
	rm dumpfile && rm dumpfile.db
