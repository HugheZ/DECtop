# DECtop
A simple python/qt app for interfacing with DECtalk

I primarily made this for tabletop RPGs in which I played as a robot, so it's suited for saving and quickly replaying saved clips.

# Requirements
1. Python. Be sure to pair your Python to the build of the dll (e.g. 32-bit Python to 32-bit dectalk.dll). You will also need a secondary 64-bit python if you want to run the DECTop UI.
2. Valid dectalk.dll and us dict file. The DECServer.py entrypoint can run registry setup as well. To find out how, run `python main.py -h`.
3. PySide6 for Qt/QtQuick 6.4.

# How to Run
Run the paired DECServer sidecar with a 32-bit python, optionally providing arguments for registry setup.

Once stable, you can either query localhost on port 8080 or run the DECTop QT frontend.

# A Note on Licenses
While DECServer will set up registry keys, it will not provide a valid license password or license count. You will need a valid license of DECtalk. If you have a setup script handy, you can instead run that. DECServer determines the location of the dectalk.dll file based on the MainDict location, so it should work with any install of DECtalk.