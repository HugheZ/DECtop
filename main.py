# This Python file uses the following encoding: utf-8
import sys
import argparse

from os import path, environ
from backend.engine.backend import QmlBackend #import so it gets registered with annotation
from backend.engine.dec import DECEngine
from backend.registry.regset import setup_dec_reg
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, QCoreApplication

def __setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Launches and optionally configures the DECtalk application")
    parser.add_argument('-s', '--setup', dest='setup', action='store_true', default=False, required=False, help='If provided, sets up the DECtalk library by setting required registry values.')
    parser.add_argument('-d', '--directory', dest='directory', action='store', default=None, type=str, required=False, help='If --setup is specified, this flag specifies an optional dectalk.dll install directory. Default <DECtop install location>/includes.')
    return parser

def __setup_env() -> None:
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    environ["QT_LOGGING_RULES"] = "qt.qml.connections=false"
    environ["QT_QUICK_CONTROLS_CONF"] = path.join(path.dirname(__file__), "qtquickcontrols2.conf")

def __add_modules(qml_engine) -> None:
    qml_engine.addImportPath("imports")
    qml_engine.addImportPath("content")

if __name__ == "__main__":
    # setup execution environment if requested
    parser = __setup_parser()
    args = parser.parse_args()
    if args.setup:
        setup_dec_reg(path.join(path.dirname(__file__), 'includes') if args.directory is None else args.directory)
    # dec = DECEngine()

    # get QML runtime
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # set up runtime env
    __setup_env()
    __add_modules(engine)

    engine.load(path.join(path.dirname(__file__), "content", "App.qml"))

    # WOO HOO needing to manually bind quit is FUN
    engine.quit.connect(QCoreApplication.quit)
    engine.quit.connect(app.quit)

    if not engine.rootObjects():
        sys.exit(-1)


    # run
    sys.exit(app.exec())

