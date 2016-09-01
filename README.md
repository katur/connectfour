# Connect Four

While inspired by
[Connect Four](https://en.wikipedia.org/wiki/Connect_Four),
this game accommodates other numbers (Connect Three, Six, etc.),
as well as variable board dimensions and a variable number of players.


## Code

The game logic is in Python.

Python version is listed in [runtime.txt](runtime.txt).

Package dependencies are listed in [requirements.txt](requirements.txt).
To install (preferably in a new [virtualenv](https://virtualenv.pypa.io)):
```
pip install -r requirements.txt
```


### Web app

The goal of the web app was to use as many "hip" technologies as I could cram
into one project:

- WebSockets, with
    [socket.io](http://socket.io/) on the client side and
    [Flask-SocketIO](https://flask-socketio.readthedocs.io/) on the server side
- Javascript uses:
  - [ES6](http://es6-features.org/#Constants) (aiming to follow
    [the Airbnb style guide](https://github.com/airbnb/javascript))
  - [React](https://facebook.github.io/react/)
  - [Redux](http://redux.js.org/)
  - [webpack](http://webpack.github.io/) to bundle for the web
- CSS uses:
  - [SASS](http://sass-lang.com/)
  - [Flexbox layout](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
  - Only [named HTML colors](http://www.crockford.com/wrrrld/color.html)
      (maybe not hip, but definitely artisanal)
- Python uses:
  - The [Flask](http://flask.pocoo.org/) framework
  - (maybe upcoming) asyncio with Python 3


To install JS dev dependencies (listed in [package.json](package.json)):
```
npm install
```

If you install any new JS dev dependencies, use the `--save-dev` option to list
in [package.json](package.json):
```
npm install <package-name> --save-dev
```

To bundle JS and CSS for the web (configured in
[webpack.config.js](webpack.config.js)):
```
webpack
```

To automate the above while developing:
```
webpack --watch
```

To launch the web app:
```
./run_web.py
```


### GUI app

The GUI view uses Python's built-in Tkinter library.

To launch:
```
./run_gui.py
```


### Command line app

To start the command line app (from root dir):
```
./run_cli.py
```



### Tests

To run all unit tests (from root dir):
```
python -m unittest discover -v
```
