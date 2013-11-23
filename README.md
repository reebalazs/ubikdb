
[![Build Status](https://travis-ci.org/reebalazs/ubikdb.png?branch=master)](https://travis-ci.org/reebalazs/ubikdb)

# ubikDB #

![](https://dl.dropboxusercontent.com/u/16162405/ubik-banner-1920.png)

This is a working title.

[Ubik](http://www.amazon.com/Ubik-Philip-K-Dick/dp/0547572298) is a book
of [Philip K. Dick](http://en.wikipedia.org/wiki/Philip_K._Dick). Maybe
they will also make a
[movie](http://screenrant.com/michel-gondry-ubik-movie-philip-dick-sandy-101655/)
out of it soon.

The Python package manager ["ubik"](https://pypi.python.org/pypi/ubik) is
unrelated with ubikDB.

## What ##

Experimenting with a concept.

## Roadmap ##

- [X] Make a clone of sdidemo with a working gevent-socketio included
- [X] Implement prefix-based (context-based) event filtering
- [X] Implement basic data binding events
- [X] Simple working demo with memory storage on the server, no persistency
- [ ] Tests
- [ ] Implement data binding events for collections
- [ ] Persistency in ZODB
- [ ] ACL
<!-- - [ ] Reconnects/ -->
- [ ] Substance-D demo

## Status ##


The demo shows the current status of the library.

The  real-time synchronized form widget of the demo is
written in only **11 lines** of HTML and **3 lines** of JavaScript code is
needed to do the data synchronization, adding up to a total of 7 lines of JS
for the entire Angular controller.

[![Play Video](https://dl.dropboxusercontent.com/u/16162405/ubikDB_1.png)](https://vimeo.com/79124531)

## History ##

### 2013-11-11 ###

- table demo added

- basic working with collections

- tests in progress

### 2013-11-02 ###

Simple working demo on top of sdidemo, capable of synchronizing
simple string values.

**This is work in progress and the early presentation of the plans and concepts.
It is very far from being ready to production.**

## Examples ##

### Substance-D based example ###

#### examples/example_substanced ####

 Use the standard buildout procedure to build
out the application.

```sh
$ $PYTHONHOME/bin/virtualenv --no-setuptools .
$ bin/python bootstrap.py
$ bin/buildout -U
```

Following this, run:

```sh
$ bin/supervisord
$ bin/pserve --reload etc/development.ini
```

Note, if you use --reload with paster, it will give an exception during startup
`NotImplementedError: gevent is only usable from a single thread`,
but otherwise it appears to work correctly.

There is a README.rst file in the example buildout directory with a lot of
more details about this procedure.

##### Using the app #####

Visit any "Document" on the retail interface (remove /manage from the url path if needed).

For example:

```
http://127.0.0.1:6541/binder_0/document_0/
```

Open it from multiple browsers or tabs, and and you should see what I showed
on the screencast.

##### Demo Architecture #####

The demo is the clone of the `sdidemo`, "sdi" stands for the
*Substance-D Development Interface* and this is the standard development environment
for Subtance-D itself. Which makes sure that we get the newest of Substance-D and
its dependencies.

The current architecture that works with the demo:

The backend is plain Python with no framework dependencies other than the database
(syncing with ZODB is in the plans). For networking, gevent-socketio is used.

I only found the repository trunk of gevent-socketio working, and the buildout
takes care that we use it from github.

The demo frontend is AngularJS. For MVC-less applications, ubikDB provides an api with
the single library dependency of the socket.io JavaScript client. On the top of this,
an MVC can implement its own bind methods.

Currently the database is volatile, this means it lives in the server's memory as long
as the application is running. Once restarted, the application resets the data.

## Discussion ##

### Initial motivation ###

I wanted to experiment with the creation of an open source library that synchronizes
data between many clients and a database server. This makes certain architectures more
interesting than the others in my eyes. I try to summarize why I took certain
decisions for the development of this package.

#### Clients ####

First of all, I am interested in the creation of a JavaScript client that runs 
in a browser. This means is the main area of my interest is supporting web 
applications with this technology.

I am also interested to see how this library can be used from AngularJS. The base
layer of the library has no dependencies, and there is an Angular specific module
that adds Angular support for that. It could be done similarly for other frameworks,
or the base layer can be used directly.

#### Server ####

On the server side, I am interested to create a Python server. My second interest would
be NodeJS. Python is more interesting for me than NodeJS, because it makes it possible
to use this database directly with other Python based server solutions, such as
Django, Pyramid, Bottle, or Plone.

#### Networking ####

- websockets, with emulation on non-html5 browsers: `socket.io`

- gevent-socketio on the server

- socket.io-client on the client

#### Data persistency ####

- ZODB

- server side procedures

- data adapters to map the json-db into the ZODB content tree

## Development of the package itself ##

### Running the tests ###

#### Python ####

To run the Python unittests, you need to perform some installation for the first time,
issued from the root directory of this package (where this README is).

```sh
$ $PYTHONHOME/bin/virtualenv --no-setuptools .
$ pip install -e '.[test]' --use-mirrors
```

This installs the package dependencies needed to run the tests into your
virtualenv.

Then, to run the Python tests, simply issue:

```sh
$ nosetests --with-coverage --cover-package=ubikdb
```

#### JavaScript ####

To run the JavaScript (unit and end-to-end) tests, you need to perform some
installation for the first time,
issued from the root directory of this package (where this README is).
You also need `node` and `npm` installed precedently on your operating system.

It is also suggested that you have the grunt cli installed globally:

```sh
$ npm install -g grunt-cli
```

Following that you can install the package dependencies needed for testing:

```sh
$ npm install .
$ grunt install
```

Then, to run the JavaScript tests, simply issue:

```sh
$ grunt test
```

This will run the tests with all the available browsers on your machine.

### Autotests ###

Meaning, it will start watching the files, and re-run the tests each time
a file has changed.

You can run the Python autotests by using `sniffer`:

```sh
$ sniffer
```

For performance improvements, install the package that it tells you at first
run (it depends on your OS).

You can run the JavaScript autotests in the following way:

```sh
$ grunt autotest
```

You can minimize the browsers that it launches, but do not close them.

If you want to debug the tests manually, do not use any of the automatically
launched browsers, but instead launch your own browser and visit:

```
http://localhost:9876/debug.html
```

### Client resources ###

Grunt by default does the installation of the resources and goes into
watch mode, which means resources autogenerated on the fly if any
of their sources have changed:

```sh
$ grunt
```

After the installation, watch mode can be enabled:

```sh
$ grunt watch
```
