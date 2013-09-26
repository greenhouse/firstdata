help:
	@echo "\033]0;firstdata\007"
	@echo "\n\033[1m------ First Data ------\033[0m \n\
	\033[1mopen\033[0m: opens project in sublime\n\
	\033[1mtest\033[0m: run unit testing\n\
	\033[1mdeploy\033[0m: tag upload\n\n\
	\t \033[94mhttps://github.com/stevepeak/firstdata\033[0m\n\
	\t\t\033[91mHappy Hacking\033[0m\n"

open:
	subl --project ~/Documents/projects/firstdata.sublime-project

deploy: tag upload

tag:
	git tag -m "" -a v$(shell grep "version = " firstdata/__init__.py | cut -d"'" -f 2)
	git push origin v$(shell grep "version = " firstdata/__init__.py | cut -d"'" -f 2)

upload:
	python setup.py sdist upload

test:
	python -m firstdata.tests
