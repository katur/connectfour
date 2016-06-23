### **Note to RC**

Gists don't allow directories, but I originally wrote this like a Python
package with some nesting. For this submission, I copied/pasted only the
relevant files into this gist. If you want to see how I would normally
organize it, the original is at:

[https://github.com/katur/connectfour](https://github.com/katur/connectfour).

There are also some unit tests and other views (including a GUI) there.


# Connect Four

While inspired by
[Connect Four](https://en.wikipedia.org/wiki/Connect_Four),
this game accommodates other numbers (Connect Three, Six, etc.),
as well as variable board dimensions and a variable number of players.


## Code

Code is in Python 2.

Package dependencies are listed in
[requirements.txt](requirements.txt). To install:
```
pip install -r requirements.txt
```


## App

To launch the app (from root dir):
```
python app.py
```
