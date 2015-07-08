# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'temp_new'
#
# Created: Tue Jul  7 13:53:51 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_InteractiveToolWidget(object):
    def setupUi(self, InteractiveToolWidget):
        InteractiveToolWidget.setObjectName(_fromUtf8("InteractiveToolWidget"))
        InteractiveToolWidget.resize(200, 184)
        self.line = QtGui.QFrame(InteractiveToolWidget)
        self.line.setGeometry(QtCore.QRect(10, 120, 181, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.nodeLabel = QtGui.QLabel(InteractiveToolWidget)
        self.nodeLabel.setGeometry(QtCore.QRect(10, 10, 62, 17))
        self.nodeLabel.setObjectName(_fromUtf8("nodeLabel"))
        self.nodeSelectionWidget = QtGui.QWidget(InteractiveToolWidget)
        self.nodeSelectionWidget.setEnabled(True)
        self.nodeSelectionWidget.setGeometry(QtCore.QRect(10, 30, 181, 91))
        self.nodeSelectionWidget.setObjectName(_fromUtf8("nodeSelectionWidget"))
        self.enableSelection = QtGui.QCheckBox(self.nodeSelectionWidget)
        self.enableSelection.setGeometry(QtCore.QRect(10, 0, 94, 22))
        self.enableSelection.setChecked(False)
        self.enableSelection.setObjectName(_fromUtf8("enableSelection"))
        self.enableEdit = QtGui.QCheckBox(self.nodeSelectionWidget)
        self.enableEdit.setGeometry(QtCore.QRect(10, 20, 94, 22))
        self.enableEdit.setObjectName(_fromUtf8("enableEdit"))
        self.enableCreate = QtGui.QCheckBox(self.nodeSelectionWidget)
        self.enableCreate.setGeometry(QtCore.QRect(10, 40, 94, 22))
        self.enableCreate.setObjectName(_fromUtf8("enableCreate"))
        self.enableConstrain = QtGui.QCheckBox(self.nodeSelectionWidget)
        self.enableConstrain.setGeometry(QtCore.QRect(10, 60, 161, 21))
        self.enableConstrain.setObjectName(_fromUtf8("enableConstrain"))
        self.elementLabel = QtGui.QLabel(InteractiveToolWidget)
        self.elementLabel.setGeometry(QtCore.QRect(10, 130, 62, 17))
        self.elementLabel.setIndent(0)
        self.elementLabel.setObjectName(_fromUtf8("elementLabel"))
        self.elementSelection = QtGui.QCheckBox(InteractiveToolWidget)
        self.elementSelection.setGeometry(QtCore.QRect(20, 150, 94, 22))
        self.elementSelection.setChecked(False)
        self.elementSelection.setObjectName(_fromUtf8("elementSelection"))

        self.retranslateUi(InteractiveToolWidget)
        QtCore.QObject.connect(self.enableSelection, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), InteractiveToolWidget.enableSelectionToggle)
        QtCore.QObject.connect(self.enableEdit, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), InteractiveToolWidget.enableEditToggle)
        QtCore.QObject.connect(self.enableCreate, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), InteractiveToolWidget.enableCreateToggle)
        QtCore.QObject.connect(self.enableConstrain, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), InteractiveToolWidget.enableConstrainToggle)
        QtCore.QObject.connect(self.elementSelection, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), InteractiveToolWidget.elementSelectionToggle)
        QtCore.QMetaObject.connectSlotsByName(InteractiveToolWidget)

    def retranslateUi(self, InteractiveToolWidget):
        InteractiveToolWidget.setWindowTitle(_translate("InteractiveToolWidget", "Form", None))
        self.nodeLabel.setText(_translate("InteractiveToolWidget", "Nodes", None))
        self.enableSelection.setText(_translate("InteractiveToolWidget", "Select", None))
        self.enableEdit.setText(_translate("InteractiveToolWidget", "Edit", None))
        self.enableCreate.setText(_translate("InteractiveToolWidget", "Create", None))
        self.enableConstrain.setText(_translate("InteractiveToolWidget", "Constrain to surfaces", None))
        self.elementLabel.setText(_translate("InteractiveToolWidget", "Elements", None))
        self.elementSelection.setText(_translate("InteractiveToolWidget", "Select", None))
