#!/usr/bin/env python

import sys
import os
import json
import re
import fnmatch

from PyQt5 import QtCore

from PyQt5 import QtWidgets, QtGui

from PyQt5.QtWidgets import QMessageBox

from pynwn.file.erf import Erf
from pynwn.resource import ResTypes, ContentObject

from widgets.MainWidget import MainWidget

class ErfReadThread(QtCore.QThread):
    erfLoaded = QtCore.pyqtSignal(Erf)

    def __init__(self, parent=None):
        super(ErfReadThread, self).__init__(parent)

    def setFileName(self, name):
        self.file_name = name

    def run(self):
        try:
            erf = Erf.from_file(self.file_name)
        except:
            erf = Erf('hak')
        self.erfLoaded.emit(erf)

    def begin(self):
        self.start()

class ErfSortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(ErfSortFilterProxyModel, self).__init__(parent)
        self.filters = {}

    def setFilter(self, idx, pat):
        if len(pat):
            self.filters[idx] = pat
        else:
            self.filters.pop(idx, None)
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        if 1 in self.filters:
            idx = self.sourceModel().index(sourceRow, 1, sourceParent)
            if not re.match(self.filters[1], idx.data()):
                return False
        if 0 in self.filters:
            idx = self.sourceModel().index(sourceRow, 0, sourceParent)
            if not fnmatch.fnmatch(idx.data(), self.filters[0]):
                return False

        return True

class ErfGridModel(QtCore.QAbstractTableModel):
    columnNames = ['Resource', 'Type', 'Size (bytes)']

    def __init__(self, erf, parent=None, *args):
        super(ErfGridModel, self).__init__()
        self.erf = erf

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.erf)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 3

    def data(self, index, role=QtCore.Qt.DisplayRole):
        i = index.row()
        j = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            co = self.erf.get_content_object(i)
            if j == 0:
                return co.resref
            elif j == 1:
                return ResTypes[co.res_type]
            elif j == 2:
                return co.size
        elif role == QtCore.Qt.TextAlignmentRole:
            if j == 1 or j == 2:
                return QtCore.Qt.AlignCenter
        else:
            return QtCore.QVariant()

    def flags(self, index):
        defaultFlags = QtCore.QAbstractTableModel.flags(self, index)
        if index.isValid():
            return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | defaultFlags
        else:
            return QtCore.Qt.ItemIsDropEnabled | defaultFlags;

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.columnNames[section]

    def setData(self, index, value, role):
        if not index.isValid() or role != QtCore.Qt.EditRole: return False
        i = index.row()
        j = index.column()

        return False

    def addFiles(self, files):
        for f in files:
            self.erf.add_file(f)
        self.layoutChanged.emit()

    def deleteFiles(self, files):
        if not len(files): return
        for f in files:
            self.erf.remove(f)
        self.layoutChanged.emit()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.settings = QtCore.QSettings('ErfEd.ini', QtCore.QSettings.IniFormat)
        self.recentFiles = []
        self.readSettings()
        self.current_row = 0
        self.mainWidget = MainWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.filterEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('([a-zA-Z0-9_\?\*]+ ?)*')))
        self.mainWidget.resourceTable.needNewErf.connect(self.newErf)
        self.grid_model = None
        self.proxy = None
        self.modified = False
        self.fileName = None
        self.current_stack = 0
        self.createActions()
        self.createMenus()
        self.initTypeCombo()
        self.setWindowTitle("ErfEd")
        self.resize(500, 600)
        self.thread = ErfReadThread(self)
        self.thread.erfLoaded.connect(self.erfReady)
        hh = self.mainWidget.resourceTable.horizontalHeader()
        hh.sectionClicked.connect(self.onHeaderSectionClicked)
        self.mainWidget.descriptionText.textChanged.connect(self.descrptionChanged)

    def onPreviousButton(self):
        if self.current_row == 0: return
        self.current_row -= 1
        self.changeRow(self.current_row)

    def onNextButton(self):
        if self.current_row + 1 >= len(self.erf.rows): return
        self.current_row += 1
        self.changeRow(self.current_row)

    def changeRow(self, row):
        self.row_model.setRow(row)
        self.current_row = row

    def openErfFile(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         "Open Erf File", '',
                                                         "ERF Files (*.erf *.mod *.hak)")
        if fname:
            self.open(fname)

    def openRecent(self):
        act = self.sender()
        if not act is None:
            fname = act.data()
            self.open(fname)

    def newErf(self):
        self.setErfObject(Erf('HAK'))

    def erfReady(self, erf):
        self.setErfObject(erf)
        self.progress.hide()
        self.progress = None

    def open(self, fname):
        if self.modified and self.checkSave() == QMessageBox.Save:
            self.save()

        self.fileName = fname
        self.progress = QtWidgets.QProgressDialog('Loading...', None, 0, 0, self, QtCore.Qt.SplashScreen)
        self.progress.setValue(0)
        self.progress.show()
        self.setErfObject(Erf('HAK'))
        self.thread.setFileName(self.fileName)
        self.thread.begin()

        self.recentFiles = [f for f in self.recentFiles if f.lower() != self.fileName.lower()]

        if len(self.recentFiles) >= 10:
            self.recentFiles.pop()

        self.recentFiles.insert(0, self.fileName)
        for i, fname in enumerate(self.recentFiles):
            self.recentFileActs[i].setText("&%d - %s" % (i+1, fname))
            self.recentFileActs[i].setData(fname)
            self.recentFileActs[i].setVisible(True)


    def about(self):
        QtWidgets.QMessageBox.about(self, "About Erf",
                                    "Edit Erf files")

    def createActions(self):
        self.newErfFileAct = QtWidgets.QAction("&New", self,
                                                shortcut="Ctrl+N",
                                                triggered=self.newErf)

        self.openErfFileAct = QtWidgets.QAction("&Open", self,
                                                shortcut="Ctrl+O",
                                                triggered=self.openErfFile)

        self.saveAct = QtWidgets.QAction("&Save", self,
                                         shortcut="Ctrl+S", triggered=self.save)

        self.saveAsAct = QtWidgets.QAction("Save As...", self,
                                           shortcut="Ctrl+Alt+S", triggered=self.saveAs)

        self.exitAct = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                                         triggered=self.close)

        self.aboutAct = QtWidgets.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtWidgets.QAction("About &Qt", self,
                                            triggered=QtWidgets.QApplication.instance().aboutQt)

        self.exportAct = QtWidgets.QAction("&Export", self,
                                        shortcut="Ctrl+E",
                                        triggered=self.export)

        self.exportAllAct = QtWidgets.QAction("Export All", self, triggered=self.exportAll)

    def export(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Export To...'
                                                          '.')
        select = self.mainWidget.resourceTable.selectionModel().selectedRows()
        for s in select:
            idx = self.mainWidget.resourceTable.model().index(s.row(), 0)
            resref = idx.data()
            idx = self.mainWidget.resourceTable.model().index(s.row(), 1)
            ext = idx.data()
            fname = '%s.%s' % (resref, ext)
            co = self.erf.get_content_object(fname)
            co.write_to(os.path.join(path, fname))

    def exportAll(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Export To...'
                                                          '.')
        for co in self.erf.content:
            co.write_to(os.path.join(path, co.get_filename()))

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newErfFileAct)
        self.fileMenu.addAction(self.openErfFileAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.recentMenu = self.fileMenu.addMenu('Recent')

        self.recentFileActs = []
        for i in range(10):
            act = QtWidgets.QAction(self)
            act.setVisible(False)
            act.triggered.connect(self.openRecent)
            self.recentMenu.addAction(act)
            self.recentFileActs.append(act)

        for i, fname in enumerate(self.recentFiles):
            self.recentFileActs[i].setText("&%d - %s" % (i+1, fname))
            self.recentFileActs[i].setData(fname)
            self.recentFileActs[i].setVisible(True)

        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.resMenu = self.menuBar().addMenu("&Resource")
        self.resMenu.addAction(self.exportAct)
        self.resMenu.addAction(self.exportAllAct)

        self.mainWidget.typeCombo.currentIndexChanged.connect(self.onTypeComboChanged)
        self.mainWidget.filterEdit.editingFinished.connect(self.onFilterChanged)
        self.menuBar().addSeparator()
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def onTypeComboChanged(self, idx):
        if not self.proxy is None:
            text = self.mainWidget.typeCombo.currentText()
            if text == 'All':
                self.proxy.setFilter(1, '')
            else:
                self.proxy.setFilter(1, text)

    def onFilterChanged(self):
        if not self.proxy is None:
            self.proxy.setFilter(0, self.mainWidget.filterEdit.text())

    def updateModels(self, erf):
        # Grid model
        self.grid_model = ErfGridModel(erf)
        self.proxy = ErfSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.grid_model)
        self.proxy.sort(0)
        self.mainWidget.resourceTable.setModel(self.proxy)
        self.mainWidget.typeCombo.setCurrentIndex(0)
        self.grid_model.layoutChanged.connect(self.changed)
        self.loaded = False
        hh = self.mainWidget.resourceTable.horizontalHeader()
        hh.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

    def onHeaderSectionClicked(self, idx):
        if self.proxy.sortOrder() == QtCore.Qt.AscendingOrder:
            order = QtCore.Qt.DescendingOrder
        else:
            order = QtCore.Qt.AscendingOrder

        self.proxy.sort(idx, order)

    def setErfObject(self, erf):
        self.erf = erf
        self.mainWidget.descriptionText.setPlainText(erf.description(0))
        self.updateModels(erf)
        self.setModified(False)

    def descrptionChanged(self):
        if self.erf.description(0) != self.mainWidget.descriptionText.toPlainText():
            self.erf.set_description(self.mainWidget.descriptionText.toPlainText(), 0)
            self.setModified(True)

    def changed(self):
        self.setModified(True)

    def initTypeCombo(self):
        self.mainWidget.typeCombo.addItem('All')
        self.mainWidget.typeCombo.addItems(sorted([v for _, v in ResTypes.items()]))

    def setModified(self, modified):
        self.modified = modified
        if self.fileName is None:
            self.setWindowTitle("ErfEd - unnamed*")
        elif modified:
            self.setWindowTitle("ErfEd - %s*" % os.path.basename(self.fileName))
        else:
            self.setWindowTitle("ErfEd - %s" % os.path.basename(self.fileName))

    def save(self):
        if self.erf is None: return
        if not self.fileName:
            self.saveAs()
        else:
            with open(self.fileName, 'wb') as f2:
                self.erf.write_to(f2)
            self.setModified(False)

    def saveAs(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Open Erf File",
                                                            self.fileName,
                                                            "ERF Files (*.hak *.mod *.erf)")

        if fileName:
            ext = os.path.splitext(fileName)[1][1:].upper()
            if self.erf.ftype != ext and ext in Erf.TYPES:
                self.erf.ftype = ext

            with open(fileName, 'wb') as f2:
                self.erf.write_to(f2)

            self.setModified(False)
            self.open(fileName)

    def readSettings(self):
        size = self.settings.beginReadArray('Recent Files')
        for i in range(size):
            self.settings.setArrayIndex(i)
            self.recentFiles.append(self.settings.value('file'))
        self.settings.endArray()


    def writeSettings(self):
        self.settings.beginWriteArray('Recent Files', len(self.recentFiles))
        for i, fname in enumerate(self.recentFiles):
            self.settings.setArrayIndex(i)
            self.settings.setValue('file', fname)
        self.settings.endArray()
        self.settings.setValue("Window/geometry", self.saveGeometry())

    def restoreWindow(self):
        geom = self.settings.value("Window/geometry")
        if not geom is None:
            self.restoreGeometry(geom)

    def checkSave(self):
        msgBox = QMessageBox()
        msgBox.setText("The file has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        return msgBox.exec()

    def closeEvent(self, event):
        if self.modified:
            ret = self.checkSave()
            if ret == QMessageBox.Save:
                self.save()
            elif ret == QMessageBox.Cancel:
                event.ignore()

        self.writeSettings()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.restoreWindow()
    if len(sys.argv) > 1:
        f = QtCore.QFileInfo(os.path.abspath(sys.argv[1]))
        mainWin.open(f.filePath())
    mainWin.show()
    app.exec()
