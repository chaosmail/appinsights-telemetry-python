APPINSIGHTS_KEY ?=

setup:
	python -m pip install --user pipenv

install:
	pipenv install

run:
	pipenv run python appinsights_telemetry_logger/command_line.py -k $(APPINSIGHTS_KEY) -l 1 --print --cpu-stats --virtual-memory --disk-usage

upload:
	python setup.py register sdist upload
