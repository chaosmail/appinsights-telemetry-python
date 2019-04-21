APPINSIGHTS_KEY ?=

setup:
	python -m pip install --user pipenv

install:
	pipenv install

run:
	pipenv run python main.py -k $(APPINSIGHTS_KEY) --print --cpu-stats --virtual-memory --disk-usage
