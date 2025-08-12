# deepcut - find profiles in ocean pressure data

Under construction.

# Building the documentation locally

To build and serve the documentation locally:

1. (Recommended) Create a separate environment for docs:
	```sh
	uv venv .venv-docs
	source .venv-docs/bin/activate
	```

2. Install documentation requirements and the package:
	```sh
    uv pip install --upgrade pip
	pip install -r docs/requirements.txt
	pip install -e .
	```

3. Build the documentation:
	```sh
	cd docs
	make html
	```

4. Serve the documentation locally:
	```sh
	python -m http.server --directory _build/html 8000
	# Then open http://localhost:8000 in your browser
	```

For live-reloading during edits, you can use:
```sh
sphinx-autobuild . _build/html
```
