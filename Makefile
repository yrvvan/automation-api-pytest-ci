global-login:
	python helpers/single_sign_on.py

test-all-json:
	pytest -s -v --json-report --json-report-file=report.json
test-get-json:
	pytest -s -m get -v --json-report --json-report-file=report.json
test-post-json:
	pytest -s -m post -v --json-report --json-report-file=report.json

test-all-html:
	pytest -s -v --html=report.html
test-get-html:
	pytest -s -m get -v --html=report.html
test-post-html:
	pytest -s -m post -v --html=report.html

notify:
	python helpers/report_generator.py
html:
	python helpers/html_viewer.py

e2e-all-json: global-login test-all-json
e2e-get-json: global-login test-get-json
e2e-post-json: global-login test-post-json

e2e-all-html: global-login test-all-html
e2e-get-html: global-login test-get-html
e2e-post-html: global-login test-post-html