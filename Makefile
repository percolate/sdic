develop:
	python setup.py develop

undevelop:
	python setup.py develop --uninstall

test:
	flake8 sdic

clean:
	rm -rf dist/

release: clean
	python setup.py sdist
	twine upload dist/*
