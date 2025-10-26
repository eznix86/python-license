.PHONY: run

run:
	@uv run python -m license || true

publish:
	source ./.env
	@uv publish --repository testpypi
