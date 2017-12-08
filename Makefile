.PHONY: check-env

run: check-env init 
	source venv/bin/activate && python gource.py

init: check-env venv stage stage/repo stage/avatars

stage:
	mkdir -p stage

stage/repo:
	git clone $(REPO_URL) stage/repo

stage/avatars:
	mkdir -p stage/avatars

venv:
	virtualenv -p python3 venv
	source venv/bin/activate && pip install requests

check-env:
ifndef REPO_URL
    $(error REPO_URL is undefined)
endif

clean:
	rm -rf venv
	rm -rf stage
