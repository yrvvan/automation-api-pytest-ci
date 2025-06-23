test-all:
	pytest -v --json-report --json-report-file=report.json
test-get:
	pytest -m get -v --json-report --json-report-file=report.json
test-post:
	pytest -m post -v --json-report --json-report-file=report.json

notify:
	python helpers/report_generator.py

all: test-all notify