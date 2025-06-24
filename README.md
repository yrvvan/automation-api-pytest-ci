# AUTOMATION API

This repository implement API Automation testing using Pytest. More about Pytest documentation can be read [here](https://docs.pytest.org/en/stable/)

## Table of Contents

- [Prerequisites](./README.md#prerequisites)
- [Installation](./README.md#installation)
- [Running the Tests](./README.md#running-the-tests)
- [Folder Structure](./README.md#folder-structure)
- [CI/CD Integration](./README.md#cicd-integration)
- [Reporting](./README.md#reporting)
- [Troubleshooting](./README.md#troubleshooting)

## Prerequisites

Install prerequisites below before getting started:

Windows & MacOS :
- Python (v3.12): You can download it [here](https://www.python.org/downloads/) and don't forget to add to `PATH` environment variables
- Verify your installation by run this command

```bash
python --version
```

## Installation

To get started with this project, follow these installation steps:

### Clone the repository

```bash
git clone https://github.com/yrvvan/automation-api-pytest-ci
cd automation-api-pytest-ci
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Verify and Open Pytest

```bash
pytest --version
```

## Running the Tests

You can run within report generator
```bash
pytest -v --json-report --json-report-file=report.json
```

or you can run it by `Makefile`
```bash
e2e-all-notify
```
This will generate report in json format and send the success rate summary into slack
or
```bash
e2e-all-html
```
This will generate report in html format and open the html report

## Folder Structure

automation-api-pytest-ci folder structure will looks like this:

```bash
/.github
  /workflows
    - pytest-pipeline.yml
/fixtures
  /schema
    - json-schema.json
  /data
    - data_test.json
/helpers
    - report_generator.py
    - validator.py
/tests
    - api_test.py
- .gitignore
- .env
- conftest.py
- Makefile
- pytest.ini
- README.md
- requirements.txt
```

## CI/CD Integration

Pytest is integrated into Github Workflows pipelines in [here](https://github.com/yrvvan/automation-api-pytest-ci/actions)

Before create PR, create prefix branch name, commit message, and title based on guidance below:

### Create New Branch Convention

```bash
Branch Name → feat/post-create-user
``` 

```bash
Example Prefix:

feat/: create new users for merchant Alibaba
test/: add new test case for create new users for merchant Alibaba
fix/: resolve issue where scenario create user failed
chore/: refactor API reporter handling logic
docs/: update fixture for new data test, readme, or other documentation
```

### Commit Message & PR Convention

```bash
Commit Message and Title PR → feat: Create new users for merchant Alibaba
Description PR → Create new scenario for create new users for merchant Alibaba
Link Ticket → https://yourcompany.jira.com/TASK-1
Reviewer → Irwan Rosyadi
Report → Attached slack success rate summary notification after testing on local environment
``` 

## Reporting

This project using 2 reporters:

- html to generate HTML format
- json to generate JSON format

## Troubleshooting

If you encounter issues with Pytest, here are a few common troubleshooting tips:

- Pytest failed to run → Ensure your Python version and dependencies is compatible (v3.12.0) and that you've installed all dependencies with pip install.
- Failed tests → If tests are failing intermittently, check the network conditions or environment setup.
For more troubleshooting steps, visit the Pytest version guide from [here](https://docs.pytest.org/en/stable/backwards-compatibility.html#python-version-support)
