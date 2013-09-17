from setuptools import setup, find_packages
import sys, os

version = '0.4'

setup(name='firstdata',
      version=version,
      description="Unofficial First Data G4 Handlers",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='firstdata gateway credit creditcard g4 processing',
      author='@iopeak',
      author_email='steve@stevepeak.net',
      url='https://github.com/stevepeak/firstdata',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages = ['firstdata'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
