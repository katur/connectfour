# Connect Four

While inspired by
[Connect Four](https://en.wikipedia.org/wiki/Connect_Four),
this game accommodates other numbers (Connect Three, Six, etc.),
as well as variable board dimensions and a variable number of players.


## Code

Code is in Python.

Python version listed in [runtime.txt](runtime.txt).

Package dependencies are listed in [requirements.txt](requirements.txt).
To install (preferably in a new [virtualenv](https://virtualenv.pypa.io)):
```
pip install -r requirements.txt
```

The GUI view uses Python's built-in Tkinter library.

The web view uses Flask, with React with Redux on the front end.
It also uses the WebSocket protocol, with
[socket.io](http://socket.io/) on the client side and
[Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) on the
server side.


## Dev

To do development work on the web app, first install Node packages:
```
npm install
```

And then start webpack to compile JS and CSS:
```
webpack --watch
```


## App

To start the command line app (from root dir):
```
python commandline_app.py
```

To start the GUI app (from root dir):
```
python gui_app.py
```

To start the web app (from root dir):
```
python web_app.py
```


## Tests

To run all unit tests (from root dir):
```
python -m unittest discover -v
```
