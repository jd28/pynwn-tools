from PyQt5 import QtCore, QtWidgets

from .ui_MainWidget import Ui_Form
from .erf_table_view import ErfTableView


class MainWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.resourceTable = ErfTableView(self.widget_2)
        self.gridLayout_4.addWidget(self.resourceTable, 3, 0, 1, 2)
