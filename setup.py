from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

install_requires = [
      'pretty-json',
      'Pygments',
      'pygments-json',
      'pygments-solarized',
      'requests'
]

setup(name='playable',
      version='1.0',
      description='Playout assets tool',
      author='Alan So',
      author_email='alansoandso@gmail.com',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
      include_package_data=True,
      entry_points={'console_scripts': ['playable = tool.playable:command_line_runner', ]},
      install_requires=install_requires
      )


