# deepcut - find profiles in ocean pressure data

See the [documentation](oceancascades.github.io/deepcut).

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

4. Serve the documentation locally (also runs the build step):
	```sh
	make serve
	# Then open http://localhost:8000 in your browser
	```
