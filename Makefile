develop:
	python setup.py develop

undevelop:
	python setup.py develop --uninstall

test:
	flake8 sdic

clean:
	rm -rf dist/
	rm -rf sql_data_integrity_checker.egg-info

release: clean
	python setup.py sdist
	twine upload dist/*
