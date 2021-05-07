#!/usr/bin/python3

import os
from setuptools import setup, find_packages, Extension

from Cython.Build import cythonize


extensions = [
    Extension(name="utils", sources=["src/utils.pyx"], extra_compile_args=["-O3"]),
    Extension(name="LocalSearch", sources=["src/LocalSearch.pyx"], extra_compile_args=["-O3"]),
    Extension(name="TabuSearch", sources=["src/TabuSearch.pyx"], extra_compile_args=["-O3"]),
    Extension(name="TwoOpt", sources=["src/TwoOpt.pyx"], extra_compile_args=["-O3"]),
]


compiler_directives = {"language_level": 3, "embedsignature": True}
extensions = cythonize(extensions, compiler_directives=compiler_directives,  build_dir="build")


setup(
    ext_modules=extensions
)