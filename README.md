# Connect Four

While inspired by
[Connect Four](https://en.wikipedia.org/wiki/Connect_Four),
this game accommodates other numbers
(Connect Three, Connect Six, etc.),
as well as variable board dimensions.


## Code

Code is in Python.

Package dependencies are listed in
[requirements.txt](requirements.txt). To install:
```
pip install -r requirements.txt
```

GUI uses Python's built-in Tkinter library.


## App

To launch GUI app (from root dir):
```
python gui_app.py
```

To launch command line app (from root dir):
```
python commandline_app.py
```


## Tests

To run all unit tests (from root dir):
```
python -m unittest discover -v
```
