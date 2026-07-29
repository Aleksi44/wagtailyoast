start:
	python manage.py runserver 0.0.0.0:4243

shell:
	python manage.py shell

mm:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

# Requires Node 12 for `yarn build` (node-sass 4.x has no prebuilt
# bindings for newer runtimes). If your Node is newer, push a version
# tag instead and download the `dist` artifact built by the Release
# workflow, then run `python -m twine upload dist/*`.
deploy:
	rm -rf dist/*
	rm -rf wagtailyoast/static/wagtailyoast/dist
	yarn build
	python -m build
	python -m twine upload dist/*

patch:
	npm version patch
	git push --tags origin master
