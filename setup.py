import os
from setuptools import setup, find_packages

version = '0.1'
README = os.path.join(os.path.dirname(__file__),'README')
long_description = open(README).read() + '\n\n'

setup(name='pytodo',
	  version = version,
	  description = 'TODO file generator from python scripts',
	  classifiers = ["Programming Language :: Python",
	  				 "Intended Audience :: Developers",
	  				 "License :: MIT",	  				 
	  				],
	  keywords='todo pytodo',
	  author='Beshr Kayali',
	  author_email='beshrkayali@gmail.com',
	  url='http://github.com/beshrkayali/pytodo',
	  license='GPL',
	  packages=find_packages(),
	  namespace_packages=['pytodo'],
	  )
