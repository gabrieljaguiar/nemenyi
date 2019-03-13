from setuptools import setup

with open('requirements.txt') as f:
    requirements = [p.strip() for p in f.readlines()]

setup(name='nemenyi',
      version='0.1.0',
      description='Library to performe Friedman test and the Nemenyi post-hoc analysis',
      url='https://github.com/gabrielj12/nemenyi',
      author='Gabriel Jonas and Victor Turrisi',
      license='MIT',
      packages=['nemenyi'],
      install_requires=requirements,
      include_package_data=True,
      zip_safe=False)
