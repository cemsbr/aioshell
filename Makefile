doc-auto:
	while true; do \
	    inotifywait -re modify aioshell doc; \
	    make doc-rebuild; \
	done

doc-rebuild:
	make -C doc clean html

clean:
	python setup.py clean
	rm -rf aioshell.egg-info/ build/ dist/
	make -C doc clean

pypi:
	python setup.py sdist upload
