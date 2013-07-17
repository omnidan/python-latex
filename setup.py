#!/usr/bin/env python

from distutils.core import setup
from latex import __version__

setup(name='python-latex',
      version=__version__,
      description='python-latex: parsing and modifying LaTeX documents with python',
      author='Daniel Bugl',
      author_email='daniel.bugl@touchlay.com',
      maintainer='Daniel Bugl',
      maintainer_email='daniel.bugl@touchlay.com',
      url='https://github.com/omnidan/python-latex',
      packages=['latex'],
      long_description="parsing and modifying LaTeX documents with python",
      license="BSD",
      platforms=["any"],
     )