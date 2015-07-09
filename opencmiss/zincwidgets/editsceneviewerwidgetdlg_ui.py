# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editsceneviewerwidget.ui'
#
# Created: Thu Jul  9 11:12:28 2015
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

class Ui_EditSceneviewerWidgetDlg(object):
    def setupUi(self, EditSceneviewerWidgetDlg):
        EditSceneviewerWidgetDlg.setObjectName(_fromUtf8("EditSceneviewerWidgetDlg"))
        EditSceneviewerWidgetDlg.resize(200, 184)
        self.line = QtGui.QFrame(EditSceneviewerWidgetDlg)
        self.line.setGeometry(QtCore.QRect(10, 120, 181, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.nodeLabel = QtGui.QLabel(EditSceneviewerWidgetDlg)
        self.nodeLabel.setGeometry(QtCore.QRect(10, 10, 62, 17))
        self.nodeLabel.setObjectName(_fromUtf8("nodeLabel"))
        self.ControlnWidget = QtGui.QWidget(EditSceneviewerWidgetDlg)
        self.ControlnWidget.setEnabled(True)
        self.ControlnWidget.setGeometry(QtCore.QRect(10, 30, 181, 91))
        self.ControlnWidget.setObjectName(_fromUtf8("ControlnWidget"))
        self.enableSelection = QtGui.QCheckBox(self.ControlnWidget)
        self.enableSelection.setGeometry(QtCore.QRect(10, 0, 94, 22))
        self.enableSelection.setChecked(False)
        self.enableSelection.setObjectName(_fromUtf8("enableSelection"))
        self.enableEdit = QtGui.QCheckBox(self.ControlnWidget)
        self.enableEdit.setGeometry(QtCore.QRect(10, 20, 94, 22))
        self.enableEdit.setObjectName(_fromUtf8("enableEdit"))
        self.enableCreate = QtGui.QCheckBox(self.ControlnWidget)
        self.enableCreate.setGeometry(QtCore.QRect(10, 40, 94, 22))
        self.enableCreate.setObjectName(_fromUtf8("enableCreate"))
        self.enableConstrain = QtGui.QCheckBox(self.ControlnWidget)
        self.enableConstrain.setGeometry(QtCore.QRect(10, 60, 161, 21))
        self.enableConstrain.setObjectName(_fromUtf8("enableConstrain"))
        self.elementLabel = QtGui.QLabel(EditSceneviewerWidgetDlg)
        self.elementLabel.setGeometry(QtCore.QRect(10, 130, 62, 17))
        self.elementLabel.setIndent(0)
        self.elementLabel.setObjectName(_fromUtf8("elementLabel"))
        self.elementSelection = QtGui.QCheckBox(EditSceneviewerWidgetDlg)
        self.elementSelection.setGeometry(QtCore.QRect(20, 150, 94, 22))
        self.elementSelection.setChecked(False)
        self.elementSelection.setObjectName(_fromUtf8("elementSelection"))

        self.retranslateUi(EditSceneviewerWidgetDlg)
        QtCore.QObject.connect(self.enableSelection, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), EditSceneviewerWidgetDlg.enableSelectionToggle)
        QtCore.QObject.connect(self.enableEdit, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), EditSceneviewerWidgetDlg.enableEditToggle)
        QtCore.QObject.connect(self.enableCreate, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), EditSceneviewerWidgetDlg.enableCreateToggle)
        QtCore.QObject.connect(self.enableConstrain, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), EditSceneviewerWidgetDlg.enableConstrainToggle)
        QtCore.QObject.connect(self.elementSelection, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), EditSceneviewerWidgetDlg.elementSelectionToggle)
        QtCore.QMetaObject.connectSlotsByName(EditSceneviewerWidgetDlg)

    def retranslateUi(self, EditSceneviewerWidgetDlg):
        EditSceneviewerWidgetDlg.setWindowTitle(_translate("EditSceneviewerWidgetDlg", "Form", None))
        self.nodeLabel.setText(_translate("EditSceneviewerWidgetDlg", "Nodes", None))
        self.enableSelection.setText(_translate("EditSceneviewerWidgetDlg", "Select", None))
        self.enableEdit.setText(_translate("EditSceneviewerWidgetDlg", "Edit", None))
        self.enableCreate.setText(_translate("EditSceneviewerWidgetDlg", "Create", None))
        self.enableConstrain.setText(_translate("EditSceneviewerWidgetDlg", "Constrain to surfaces", None))
        self.elementLabel.setText(_translate("EditSceneviewerWidgetDlg", "Elements", None))
        self.elementSelection.setText(_translate("EditSceneviewerWidgetDlg", "Select", None))
