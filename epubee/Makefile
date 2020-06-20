proxy:
	mitmdump -w dumpfile --anticache

export:
	mitmdump -ns export_html_addon.py -r dumpfile

gen_html:
	pipenv run python assemble_book.py

convert:
	python3 convert.py

clean:
	rm dumpfile && rm *.html && rm *.mobi
