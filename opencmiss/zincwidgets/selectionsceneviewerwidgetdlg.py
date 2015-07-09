#!/usr/bin/python
"""
PyZinc examples

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

Created on July 9, 2015

@author: Alan Wu
"""

import sys
try:
    from PySide import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui
from selectionsceneviewerwidgetdlg_ui import Ui_SelectionSceneviewerWidgetDlg
from selectionsceneviewerwidget import SelectionSceneviewerWidget

class SelectionSceneviewerWidgetDlg(QtGui.QWidget):
    
    def __init__(self, selectionsceneviewerwidget, parent=None):
        '''
        Initiaise the interactive dialog first calling the QWidget __init__ function.
        '''
        QtGui.QWidget.__init__(self, parent)
        
        # Using composition to include the visual element of the GUI.
        self.ui = Ui_SelectionSceneviewerWidgetDlg()
        self.ui.setupUi(self)
        self._selectionsceneviewerwidget = selectionsceneviewerwidget
        self._updateUI()
#        self.setWindowIcon(QtGui.QIcon(":/cmiss_icon.ico"))

    def updateCheckbox(self, checkbox, checkstate):
        checkbox.blockSignals(True)
        checkbox.setChecked(checkstate)
        checkbox.blockSignals(False)

    def _updateUI(self):
        self.updateCheckbox(self.ui.enableSelection, self._selectionsceneviewerwidget._nodeSelectMode)
        self.updateCheckbox(self.ui.elementSelection, self._selectionsceneviewerwidget._elemSelectMode)

    def enableSelectionToggle(self):
        self._selectionsceneviewerwidget.selectionSettingsChanged.disconnect(self._updateUI)
        self._selectionsceneviewerwidget.setNodeSelection(self.ui.enableSelection.isChecked())
        self._selectionsceneviewerwidget.selectionSettingsChanged.connect(self._updateUI)
        
    def elementSelectionToggle(self):
        self._selectionsceneviewerwidget.selectionSettingsChanged.disconnect(self._updateUI)
        self._selectionsceneviewerwidget.etElementSelection(self.ui.elementSelection.isChecked())
        self._selectionsceneviewerwidget.selectionSettingsChanged.connect(self._updateUI)
