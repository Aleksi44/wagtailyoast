start:
	python manage.py runserver 0.0.0.0:4243 --settings='settings'

shell:
	python manage.py shell --settings='settings'

mm:
	python manage.py migrate --settings='settings'

superuser:
	python manage.py createsuperuser --settings='settings'

deploy:
	rm -rf dist/*
	yarn build
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

patch:
	npm version patch
	git push --tags origin master
