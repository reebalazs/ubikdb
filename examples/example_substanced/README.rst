UbikDB example with Substance-D
===============================

.. image:: http://tinyurl.com/mso7x2h


Buildout for SDI Development
============================

This buildout creates a suitable environment for hacking on the Substance D
SDI.  It installs a demonstration Substance D application as well as the
sources used to compile CSS/JS assets for eventual inclusion into Substance D.

Installing
----------

Check this package out of GitHub (must be a member of the Pylons organization
on the Substance D team)::

  $ git clone git@github.com:Pylons/sdidev.git

Cd into the ``sdidev`` directory.

Download virtualenv from http://pypi.python.org/pypi/virtualenv and install
it into your system Python (2.7+).  Once you've installed it, create a
virtualenv like so::

  $ $PYTHONHOME/bin/virtualenv --no-setuptools .

Where $PYTHONHOME/bin is where your Python installation installs its scripts.
This will create a virtualenv within the ``sdidev`` directory. The
--no-setuptools flag is important to make sure that buildout can use its
preferred version of setuptools instead of whatever your system Python has.

After you've succesfully done the above, invoke the buildout via::

  $ bin/python bootstrap.py
  $ bin/buildout -U

.. warning:: The ``-U`` flag above is *very important*.  It specifies
   to buildout that it should ignore the ``~/.buildout/default.cfg``
   file, which is often trampled upon by other software in ways that
   are incompatible with our usage of buildout.

When it's finished, an application named ``sdi_ubikdb_demo`` and its dependencies
(which include Substance D) should have been downloaded and compiled.  All
required Pyramid and Substance D software should also be installed within the
buildout environment.

If the buildout doesn't finish successfully due to a compilation error, make
sure you have gcc configured on your system and make sure you have the Python
development libraries installed.  For Debian-based systems, this means
installing the ``build-essential`` and ``python-devel`` (or perhaps
``python-dev``) packages.  For Mac OS X users, this means having XCode Tools
installed.  Then try again.

You should then be able to run the following commands and visit the
running application at http://127.0.0.1:6541 in a browser.  You may
log in as ``admin`` with password ``admin`` to the management interface at
http://127.0.0.1:6541/manage::

  [chrism@oops sdidev]$ bin/supervisord
  [chrism@oops sdidev]$ bin/pserve etc/development.ini --reload

Success looks like this::

  [chrism@oops sdidev]$ bin/supervisord
  [chrism@thinko sdidev]$ bin/pserve etc/development.ini --reload
  Starting subprocess with file monitor
  2012-03-21 14:47:15,711 INFO  [ZEO.ClientStorage][MainThread] ('localhost', 9993) ClientStorage (pid=20128) created RW/normal for storage: '1'
  2012-03-21 14:47:15,713 INFO  [ZEO.cache][MainThread] created temporary cache file '<fdopen>'
  2012-03-21 14:47:15,716 INFO  [ZEO.ClientStorage][Connect([(2, ('localhost', 9993))])] ('localhost', 9993) Testing connection <ManagedClientConnection ('127.0.0.1', 9993)>
  2012-03-21 14:47:15,718 INFO  [ZEO.zrpc.Connection(C)][('localhost', 9993) zeo client networking thread] (127.0.0.1:9993) received handshake 'Z3101'
  2012-03-21 14:47:15,818 INFO  [ZEO.ClientStorage][Connect([(2, ('localhost', 9993))])] ('localhost', 9993) Server authentication protocol None
  2012-03-21 14:47:15,819 INFO  [ZEO.ClientStorage][Connect([(2, ('localhost', 9993))])] ('localhost', 9993) Connected to storage: ('localhost', 9993)
  2012-03-21 14:47:15,820 INFO  [ZEO.ClientStorage][Connect([(2, ('localhost', 9993))])] ('localhost', 9993) No verification necessary -- empty cache
  Starting server in PID 20128.
  serving on http://0.0.0.0:6541

The ``supervisord`` command starts the ZEO server (and any other required
processes, delta the actual Substance D app).  The application will not work
without the ZEO server running.  You can use ``bin/supervisorctl`` to get a
Supervisor shell to start and stop the ZEO server.  The
``etc/supervisord.conf`` file contains Supervisor configuration.

The ``bin/py`` command within the buildout directory will invoke an
interactive Python prompt with all the ``substanced`` dependencies available
for import.

Log files, pid files, and database files are stored in the ``var`` directory.

Installing Node and LESS
------------------------

To deal with compiling resources, you need both node.js and the LESS compiler
installed on your system.  On a Ubuntu Linux machine, these can be installed
via::

  sudo apt-get install npm
  sudo npm install -g less

You should wind up with a ``lessc`` executable on the path.  Version 1.3.1
seems to work to compile things.  Version 1.2.1 seemed to fail with a similar
error to this one for me https://github.com/cloudhead/less.js/issues/906

You can see the version of less you have by doing ``lessc -v``.

Updating Sources
----------------

To update checked out source packages, you can either use "git pull" within
the source directory (e.g. within ``src/substanced``) or you can use the
``develop up`` command from within the buildout directory::

  bin/develop up substanced

You can update all checked out packages by using::

  bin/develop up

This will work with any package listed in the ``buildout.cfg`` ``[sources]``
section.

The ``develop`` command has other useful options such as ``activate``,
``deactivate`` and ``info``.  See ``develop --help`` for more info.
``decactivating`` a source is useful when there's a released version of the
source and you'd rather use it than the checked out version.

Updating the Buildout
---------------------

To update the buildout, run ``git pull`` within the buildout root dir, then::

   bin/buildout

This will cause all necessary software to be upgraded and installed as per
the directions in the ``buildout.cfg`` file.

You need to do this whenever you change the ``buildout.cfg`` file or add an
``install_requires`` dependency to ``substanced`` or any other package.

Evolving the Database
---------------------

When "schema" changes need to be made to persistent objects, it will be
required to run the ``bin/evolve`` script::

  $ bin/evolve --latest etc/development.ini

This will run all required evolution scripts present in the
``substanced/evolution`` package (e.g. ``evolve1.py``, etc) and will set the
database version to the code version.

The evolution machinery uses the ``repoze.evolution`` package.

Walking Up To the System After a Few Days
-----------------------------------------

If you're a developer on the project and you need to get the software and
your database data up to date after walking away for a few days, you should
do these things::

  $ cd sdidev
  $ git pull
  $ bin/buildout
  $ bin/develop up
  $ bin/evolve --latest etc/development.ini

This should get you to a place where you're running the most current software
versions and it will apply any evolve steps to your development database.

Running Tests
-------------

TBD.
