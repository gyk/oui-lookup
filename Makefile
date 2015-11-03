
all: oui.csv

oui.csv: oui.txt
	python parse_oui.py

oui.txt:
	python download_oui.py
