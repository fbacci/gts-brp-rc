#!/usr/bin/python3

import os
from setuptools import setup, find_packages, Extension

from Cython.Build import cythonize


extensions = [
    Extension("utils", ["src/utils.pyx"]),
    Extension("LocalSearch", ["src/LocalSearch.pyx"]),
    Extension("TabuSearch", ["src/TabuSearch.pyx"]),
    Extension("TwoOpt", ["src/TwoOpt.pyx"]),
]


compiler_directives = {"language_level": 3, "embedsignature": True}
extensions = cythonize(extensions, compiler_directives=compiler_directives,  build_dir="build")


setup(
    ext_modules=extensions
)