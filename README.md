# DECtop
A simple python/qt app for interfacing with DECtalk

I primarily made this for tabletop RPGs in which I played as a robot, so it's suited for saving and quickly replaying saved clips.

# Requirements
1. Python. Be sure to pair your Python to the build of the dll (e.g. 32-bit Python to 32-bit dectalk.cll)
2. Valid dectalk.dll and us dict file. The main.py entrypoint can run registry setup as well. To find out how, run `python main.py -h`.
3. PySide6 for Qt/QtQuick 6.4.