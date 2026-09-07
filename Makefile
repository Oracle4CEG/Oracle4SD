.PHONY: lint test release-smoke release-contract reproduce-release
lint:
	python scripts/check_template.py
test:
	python -m unittest discover -s tests -v
release-smoke:
	python scripts/run_pipeline.py
release-contract:
	python scripts/check_template.py
reproduce-release:
	python scripts/run_pipeline.py
