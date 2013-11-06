
[![Build Status](https://travis-ci.org/reebalazs/ubikdb.png?branch=master)](https://travis-ci.org/reebalazs/ubikdb)

# ubikDB #

![](https://dl.dropboxusercontent.com/u/16162405/ubik-banner-1920.png)

This is a working title.

[Ubik](http://www.amazon.com/Ubik-Philip-K-Dick/dp/0547572298) is a book
of [Philip K. Dick](http://en.wikipedia.org/wiki/Philip_K._Dick). Maybe
they will also make a
[movie](http://screenrant.com/michel-gondry-ubik-movie-philip-dick-sandy-101655/)
out of it soon.

The python package manager ["ubik"](https://pypi.python.org/pypi/ubik) is
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
- [ ] Reconnects
- [ ] Substance-D demo

## Status ##

This screencast was made after the first two days of development. 
It is intended to give a peek preview into how ubikDB will work, by showing
the simplest possible use case that can operate with the current codebase.
The  real-time synchronized form widget of the demo is
written in only **11 lines** of HTML and **3 lines** of JavaScript code is
needed to do the data synchronization, adding up to a total of 7 lines of JS
for the entire Angular controller.

[![Play Video](https://dl.dropboxusercontent.com/u/16162405/ubikDB_0__starting_up.png)]( http://vimeo.com/reebalazs/ubikdb-0)

**This is work in progress and the early presentation of the plans and concepts.
It is very far from being ready to production.**

## Demos ##

##examples/example_substanced: Substance-D based example##

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
$ bin/pserve etc/development.ini
```

Do **not** use --reload with paster, it does not seem to work with gevents!

There is a README.rst file in the example buildout directory with a lot of
more details about this procedure.

###Architecture###

The demo is the clone of the "sdidemo", "sdi" stands for the
*Substance-D Development Interface*.

The current architecture that works with the demo:

The backend is plain python with no framework dependencies other than the database
(syncing with ZODB is in the plans). For networking, gevent-socketio is used.

I only found the repository trunk of gevent-socketio working, and the buildout
takes care that we use it from github.

The demo frontend is AngularJS. For MVC-less applications, ubikDB provides an api with
the single library dependency of the socket.io JavaScript client. On the top of this,
an MVC can implement its own bind methods.

Currently the database is volatile, this means it lives in the server's memory as long
as the application is running. Once restarted, the application resets the data.

###Using the app###

Visit any "Document" on the retail interface (remove /manage from the url path if needed).

For example:

    http://127.0.0.1:6541/binder_0/document_0/

Open it from multiple browsers or tabs, and and you should see what I showed
on the screencast.
