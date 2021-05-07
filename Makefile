SHELL=powershell

ifeq ($(OS),Windows_NT)
    RM = powershell rm
else
    RM = rm
endif


.PHONY: build dist redist install install-from-source clean uninstall

build:
	.venv/Scripts/python.exe ./setup.py build

dist:
	.venv/Scripts/python.exe ./setup.py sdist bdist_wheel

redist: clean dist

install:
	.venv/Scripts/python.exe -m pip install .

clean:
	$(RM) -r build/
	$(RM) -r src/__pycache__
	$(RM) -r src/*.egg-info
	$(RM) -r dist/

uninstall:
	.venv/Scripts/python.exe -m pip uninstall gts-brp-rc