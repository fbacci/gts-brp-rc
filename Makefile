SHELL=powershell

ifeq ($(OS),Windows_NT)
    RM = powershell rm -r
else
    RM = rm -f -r
endif


.PHONY: build dist redist install clean uninstall start execute

build:
	.venv/Scripts/python.exe ./setup.py build

dist:
	.venv/Scripts/python.exe ./setup.py sdist bdist_wheel

redist: clean dist

install:
	.venv/Scripts/python.exe -m pip install .

clean:
	$(RM) build/
	$(RM) src/__pycache__
	$(RM) src/*.egg-info
	$(RM) dist/

uninstall:
	.venv/Scripts/python.exe -m pip uninstall gts-brp-rc

start:
	.venv/Scripts/python.exe src/main.py

execute: build dist install start

clean-all: clean uninstall