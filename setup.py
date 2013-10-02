from setuptools import setup

setup(name='firstdata',
      version='0.8',
      description="Unofficial First Data G4 Handlers",
      long_description="",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: Apache Software License",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: Implementation :: PyPy",
                   "Topic :: Office/Business :: Financial"],
      keywords='firstdata gateway credit creditcard g4 processing',
      author='@iopeak',
      author_email='steve@stevepeak.net',
      url='https://github.com/stevepeak/firstdata',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages=['firstdata'],
      include_package_data=True,
      zip_safe=True,
      install_requires=["requests==2.0.0"],
      entry_points="")
