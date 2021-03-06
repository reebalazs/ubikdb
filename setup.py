
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1.0'

setup(name='ubikdb',
      version=version,
      description="",
      long_description=read('README.md'),
      classifiers=[
          "Environment :: Web Environment",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
      ],
      keywords='',
      author='Balazs Ree',
      author_email='ree@greenfinity.hu',
      url='https://github.com/reebalazs/ubikdb',
      license='',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=[
            'nose',
            'coverage',
            'mock',
            'sniffer',
            #
            # You should install a third-party library
            # so sniffer does not eat CPU.
            # Supported libraries are:
            # 'pyinotify',     # (Linux)
            # 'pywin32',       # (Windows)
            # 'MacFSEvents',   # (OSX)
            #
          ]
      ),
      install_requires=[
          # XXX 0.3.6rc2 does not work, needs master from github repo
          'gevent-socketio > 0.3.6rc2',
          'gevent-websocket',
          'ZODB3',
     ],
      dependency_links=[
          'http://github.com/abourget/gevent-socketio/tarball/master#egg=gevent-socketio-0.3.6rc3',
      ],
      entry_points="""
      """,
      )
