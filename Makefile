ifeq ($(OS),Windows_NT)
    RM = powershell rm -r
else
    RM = rm -f -r
endif

VENV_PATH=.venv/Scripts


.PHONY: build dist redist install clean uninstall start execute profile

build:
	${VENV_PATH}/python ./setup.py build

dist:
	${VENV_PATH}/python ./setup.py sdist bdist_wheel

redist: clean dist

install:
	${VENV_PATH}/python -m pip install .

clean:
	$(RM) build/
	$(RM) src/__pycache__
	$(RM) src/*.egg-info
	$(RM) dist/

uninstall:
	${VENV_PATH}/python -m pip uninstall gts-brp-rc

start:
	${VENV_PATH}/python src/main.py

execute: build dist install start

clean-all: clean uninstall

profile: 
	${VENV_PATH}/python -m cProfile -o program.prof src/main.py