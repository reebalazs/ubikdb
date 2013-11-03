
# ubikDB #

![](https://dl.dropboxusercontent.com/u/16162405/ubik-banner-1920.png)

This is a working title.

[Ubik](http://www.amazon.com/Ubik-Philip-K-Dick/dp/0547572298) is a book
of [Philip K. Dick](http://en.wikipedia.org/wiki/Philip_K._Dick).

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
- [ ] Substance-D demo

## Status ##

This screencast was made after the first two days of development. 
It is intended to give a peek preview into how ubikDB will work, by showing
the simplest possible use case that can operate with the current codebase.
The  real-time synchronized form widget of the demo is
written in only **11 lines** of HTML and **3 lines** of JavaScript code. 

[![Play Video](https://dl.dropboxusercontent.com/u/16162405/ubikDB_0__starting_up.png)]( http://vimeo.com/reebalazs/ubikdb-0)

**This is work in progress and the early presentation of the plans and concepts.
It is very far from being ready to production.**

## Running it ##

**examples/example_substanced:** standard buildout procedure (virtualenv, 
bootstrap, buildout). A clone of the Substance-D Development Interface (SDI).
There is a README file there with some more details.

The current architecture that works with the demo:

The backend is plain python with no framework dependencies other than the database
(syncing with ZODB is in the plans). For networking, gevent-socketio is used.

The demo frontend is AngularJS. ubikDB provides an api with the single dependency
to socket.io.

XXX

Do not use --reload with paster.
