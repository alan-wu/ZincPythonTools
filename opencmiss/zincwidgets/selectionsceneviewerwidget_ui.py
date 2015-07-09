# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectionsceneviewerwidget.ui'
#
# Created: Thu Jul  9 11:12:49 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui

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

class Ui_SelectionSceneviewerWidgetDlg(object):
    def setupUi(self, SelectionSceneviewerWidgetDlg):
        SelectionSceneviewerWidgetDlg.setObjectName(_fromUtf8("SelectionSceneviewerWidgetDlg"))
        SelectionSceneviewerWidgetDlg.resize(199, 118)
        self.nodeLabel = QtGui.QLabel(SelectionSceneviewerWidgetDlg)
        self.nodeLabel.setGeometry(QtCore.QRect(10, 10, 62, 17))
        self.nodeLabel.setObjectName(_fromUtf8("nodeLabel"))
        self.ControlWidget = QtGui.QWidget(SelectionSceneviewerWidgetDlg)
        self.ControlWidget.setEnabled(True)
        self.ControlWidget.setGeometry(QtCore.QRect(10, 30, 181, 91))
        self.ControlWidget.setObjectName(_fromUtf8("ControlWidget"))
        self.enableSelection = QtGui.QCheckBox(self.ControlWidget)
        self.enableSelection.setGeometry(QtCore.QRect(10, 0, 94, 22))
        self.enableSelection.setChecked(False)
        self.enableSelection.setObjectName(_fromUtf8("enableSelection"))
        self.line = QtGui.QFrame(self.ControlWidget)
        self.line.setGeometry(QtCore.QRect(0, 20, 181, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.elementSelection = QtGui.QCheckBox(self.ControlWidget)
        self.elementSelection.setGeometry(QtCore.QRect(10, 60, 94, 22))
        self.elementSelection.setChecked(False)
        self.elementSelection.setObjectName(_fromUtf8("elementSelection"))
        self.elementLabel = QtGui.QLabel(self.ControlWidget)
        self.elementLabel.setGeometry(QtCore.QRect(0, 40, 62, 16))
        self.elementLabel.setIndent(0)
        self.elementLabel.setObjectName(_fromUtf8("elementLabel"))

        self.retranslateUi(SelectionSceneviewerWidgetDlg)
        QtCore.QObject.connect(self.enableSelection, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), SelectionSceneviewerWidgetDlg.enableSelectionToggle)
        QtCore.QObject.connect(self.elementSelection, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), SelectionSceneviewerWidgetDlg.elementSelectionToggle)
        QtCore.QMetaObject.connectSlotsByName(SelectionSceneviewerWidgetDlg)

    def retranslateUi(self, SelectionSceneviewerWidgetDlg):
        SelectionSceneviewerWidgetDlg.setWindowTitle(_translate("SelectionSceneviewerWidgetDlg", "Form", None))
        self.nodeLabel.setText(_translate("SelectionSceneviewerWidgetDlg", "Nodes", None))
        self.enableSelection.setText(_translate("SelectionSceneviewerWidgetDlg", "Select", None))
        self.elementSelection.setText(_translate("SelectionSceneviewerWidgetDlg", "Select", None))
        self.elementLabel.setText(_translate("SelectionSceneviewerWidgetDlg", "Elements", None))

