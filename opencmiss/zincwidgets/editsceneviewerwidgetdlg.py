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
from editsceneviewerwidgetdlg_ui import Ui_EditSceneviewerWidgetDlg
from editsceneviewerwidget import EditSceneviewerWidget

class EditSceneviewerWidgetDlg(QtGui.QWidget):
    
    def __init__(self, editsceneviewerwidget, parent=None):
        '''
        Initiaise the interactive dialog first calling the QWidget __init__ function.
        '''
        QtGui.QWidget.__init__(self, parent)
        
        # Using composition to include the visual element of the GUI.
        self.ui = Ui_EditSceneviewerWidgetDlg()
        self.ui.setupUi(self)
        self._editsceneviewerwidget = editsceneviewerwidget
        self._updateUI()
        self._editsceneviewerwidget.selectionSettingsChanged.connect(self._updateUI)
#        self.setWindowIcon(QtGui.QIcon(":/cmiss_icon.ico"))

    def updateCheckbox(self, checkbox, checkstate):
        checkbox.blockSignals(True)
        checkbox.setChecked(checkstate)
        checkbox.blockSignals(False)

    def _updateUI(self):
        self.updateCheckbox(self.ui.enableSelection, self._editsceneviewerwidget._nodeSelectMode)
        self.updateCheckbox(self.ui.elementSelection, self._editsceneviewerwidget._elemSelectMode)
        self.updateCheckbox(self.ui.enableEdit, self._editsceneviewerwidget._nodeEditMode)
        self.updateCheckbox(self.ui.enableCreate, self._editsceneviewerwidget._nodeCreateMode)
        self.updateCheckbox(self.ui.enableConstrain, self._editsceneviewerwidget._nodeConstrainMode)

    def enableSelectionToggle(self):
        self._editsceneviewerwidget.selectionSettingsChanged.disconnect(self._updateUI)
        self._editsceneviewerwidget.setNodeSelection(self.ui.enableSelection.isChecked())
        self._editsceneviewerwidget.selectionSettingsChanged.connect(self._updateUI)
        
    def elementSelectionToggle(self):
        self._editsceneviewerwidget.selectionSettingsChanged.disconnect(self._updateUI)
        self._editsceneviewerwidget.setElementSelection(self.ui.elementSelection.isChecked())
        self._editsceneviewerwidget.selectionSettingsChanged.connect(self._updateUI)
             
    def enableEditToggle(self):
        self._editsceneviewerwidget.selectionSettingsChanged.disconnect(self._updateUI)
        self._editsceneviewerwidget.setNodeEdit(self.ui.enableEdit.isChecked())
        self._editsceneviewerwidget.selectionSettingsChanged.connect(self._updateUI)
            
    def enableCreateToggle(self):
        self._editsceneviewerwidget.selectionSettingsChanged.disconnect(self._updateUI)
        self._editsceneviewerwidget.setNodeCreateMode(self.ui.enableCreate.isChecked())
        self._editsceneviewerwidget.selectionSettingsChanged.connect(self._updateUI)
        
    def enableConstrainToggle(self):
        self._editsceneviewerwidget.selectionSettingsChanged.disconnect(self._updateUI)
        self._editsceneviewerwidget.setNodeConstrainToSurfacesMode(self.ui.enableConstrain.isChecked())
        self._editsceneviewerwidget.selectionSettingsChanged.connect(self._updateUI)
