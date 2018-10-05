import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='nextinteractive-python',
      version='0.1.0',
      description='Python wrapper for NextInteractive API',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/nextinteractive-python',
      author='Nerio Rincon',
      author_email='nrincon.mr@gmail.com',
      license='GPL',
      packages=['nextinteractive'],
      install_requires=[
          'requests',
          'xmltodict',
      ],
      zip_safe=False)
