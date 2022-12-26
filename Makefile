OS := $(shell uname -s)

install: lint install-$(OS)

DARWIN_TARGET=/Volumes/CIRCUITPY
.PHONY: install-Darwin
install-Darwin:
	@if [ -e $(DARWIN_TARGET) ]; then  \
		rsync --exclude .Trashes  --exclude .metadata_never_index --exclude .fseventsd/no_log --inplace --delete -cvrlF  . $(DARWIN_TARGET)/ ; \
	else \
		echo "missing $(DARWIN_TARGET)" ; \
	fi

.PHONY: install-CYGWIN_NT-10.0
install-CYGWIN_NT-10.0:
	drive=$(shell wmic logicaldisk get deviceid, volumename | grep CIRCUITPY | cut -f1 -d':') ; \
	rsync --inplace --delete -cvrlF  . /cygdrive/$$drive/

.PHONY: update
update:
	circup update --all
	circup freeze > circup.txt

.PHONY: pip
pip:
	pip-compile
	pip-sync

.PHONY: lint
lint:
	flake8 *.py

.PHONY: reformat
reformat:
	isort *.py
	black *.py

