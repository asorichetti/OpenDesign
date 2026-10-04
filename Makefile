.PHONY: lint test build clean

lint:
	ruff check .

test:
	pytest tests/ -v

build: lint test
	@echo "Build complete"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
