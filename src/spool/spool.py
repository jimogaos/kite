#!/bin/python

from PySide import QtGui
# from PySide import QtCore

import scene_qtgraph
from os import path

import qtutils


class SpoolMainWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtGui.QMainWindow.__init__(self, *args, **kwargs)
        self.loadUi()
        self.scenes = []

        self.show()

    def addScene(self, scene):
        self.scenes.append(scene)
        self.tabs.setMovable(True)
        self.tabs.addTab(scene_qtgraph.QKiteDisplacementDock(scene),
                         'Displacement')
        self.tabs.addTab(scene_qtgraph.QKiteQuadtreeDock(scene.quadtree),
                         'Quadtree')

    def exit(self):
        pass

    def loadUi(self):
        ui_file = path.join(path.dirname(path.realpath(__file__)),
                            'ui/spool.ui')
        qtutils.loadUi(ui_file, baseinstance=self)
        return


class Spool(QtGui.QApplication):
    def __init__(self, scene=None):
        QtGui.QApplication.__init__(self, ['KiteSpool'])
        # self.setStyle('plastique')

        self.spool_win = SpoolMainWindow()

        self.aboutToQuit.connect(self.deleteLater)
        self.spool_win.actionExit.triggered.connect(self.exit)

        if scene is not None:
            self.addScene(scene)
        self.exec_()

    def addScene(self, scene):
        return self.spool_win.addScene(scene)

    def __del__(self):
        pass

__all__ = '''
Spool
'''.split()

if __name__ == '__main__':
    from kite.scene import SceneSynTest, Scene
    import sys
    if len(sys.argv) > 1:
        sc = Scene.load(sys.argv[1])
    else:
        sc = SceneSynTest.createGauss()

    Spool(scene=sc)
