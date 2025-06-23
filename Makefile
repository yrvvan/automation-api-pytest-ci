test-all:
	pytest -v --json-report --json-report-file=report.json
test-get:
	pytest -m get -v --json-report --json-report-file=report.json
test-post:
	pytest -m post -v --json-report --json-report-file=report.json

notify:
	python helpers/report_generator.py
html:
	python helpers/html_viewer.py

e2e-notify: test-all notify
e2e-html: test-all html