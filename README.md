# Simple HTTP server tutorial

This tutorial is a [step-by-step walkthrough](https://github.com/bugaevc/simple-http-server-tutorial/commits/master) of implementing a very basic HTTP server and a nanoframework for web apps in pure Python on top of bare TCP sockets.
The server won't be as advanced or feature-reach as [leek](https://github.com/bugaevc/leek) or Python's built-in [`http.server`](https://docs.python.org/3/library/http.server.html),
and the nanoframework won't be as complete as Flask, but they have enough functionality to support parsing basic GET and POST requests, dispatching them to a collection of handlers and sending back the response.

The server and nanoframework implementation takes up about 150 lines of Python code; it's followed by another 50 lines implementing a simple to-do list webapp on top of the nanoframework
to demonstrate using its API and make it possible to run and test the whole thing.
