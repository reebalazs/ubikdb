import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'substanced',
    'pyramid_tm',
    'deformdemo',
    'pyramid_multiauth',
    'ubikdb',
    ]

setup(name='sdi_ubikdb_demo',
      version='0.0',
      description='sdi_ubikdb_demo',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons substanced',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="sdi_ubikdb_demo",
      entry_points = """\
      [paste.app_factory]
      main = sdi_ubikdb_demo:main
      [console_scripts]
      qpwrapper = sdi_ubikdb_demo.scripts.qpwrapper:main
      """,
      )

