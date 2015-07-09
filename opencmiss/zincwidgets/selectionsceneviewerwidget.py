"""
Zinc Selection Sceneviewer Widget

Implements a Zinc Selection Sceneviewer Widget on Python using PySide or PyQt,
which renders the Zinc Scene with OpenGL and allows interactive
transformation of the view.
Widget is derived from QtOpenGL.QGLWidget.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
# This python module is intended to facilitate users creating their own applications that use OpenCMISS-Zinc
# See the examples at https://svn.physiomeproject.org/svn/cmiss/zinc/bindings/trunk/python/ for further
# information.

try:
    from PySide import QtCore, QtOpenGL
except ImportError:
    from PyQt4 import QtCore, QtOpenGL

from opencmiss.zinc.sceneviewer import Sceneviewer, Sceneviewerevent
from opencmiss.zinc.graphics import Graphics
from opencmiss.zinc.sceneviewerinput import Sceneviewerinput
from sceneviewerwidget import SceneviewerWidget, button_map, modifier_map
from opencmiss.zinc.scenepicker import Scenepicker
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.scenecoordinatesystem import \
        SCENECOORDINATESYSTEM_LOCAL, \
        SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT,\
        SCENECOORDINATESYSTEM_WORLD
from opencmiss.zinc.field import Field
from selectionsceneviewerwidget_ui import Ui_SelectionSceneviewerWidgetDlg


SELECTION_RUBBERBAND_NAME = 'selection_rubberband'

class SelectionMode(object):

    NONE = -1
    EXCLUSIVE = 0
    ADDITIVE = 1
    EDIT_POSITION = 2
    EDIT_VECTOR = 3
    CREATE = 4

class SelectionSceneviewerWidget(SceneviewerWidget):
    
    try:
        # PySide
        selectionSettingsChanged = QtCore.Signal()
    except AttributError:
        # PyQt
        selectionSettingsChanged = QtCore.pyqtSignal()
    
    selectionSettingsChanged = QtCore.Signal()
    
    def __init__(self, parent=None, shared=None):
        
        # Selection attributes
        SceneviewerWidget.__init__(self, parent, shared)
        self._nodeSelectMode = False
        self._dataSelectMode = False
        self._1delemSelectMode = False
        self._2delemSelectMode = False
        self._elemSelectMode = False
        self._selection_mode = SelectionMode.NONE
        self._selectionGroup = None
        self._selection_box = None
        self._selectionModifier = QtCore.Qt.SHIFT
        self._additiveSelectionModifier = QtCore.Qt.ALT
        self._sceneSurfacesFilter = None
        self._handle_mouse_events = False
       # self.ui = Ui_InteractiveToolWidget()
       # self.ui.setupUi(self)
        
    def setAdditiveSelectionModifier(self, modifierIn):
        self._additiveSelectionModifier = modifierIn
        
    def setSelectionModifier(self, modifierIn):
        self._selectionModifier = modifierIn
        
    def initializeGL(self):
        '''
        Initialise the Zinc scene for drawing the axis glyph at a point.  
        '''
        # Following throws exception if you haven't called setContext() yet
        SceneviewerWidget.initializeGL(self)
        if self._sceneviewer and self._sceneviewer.isValid():
            scene = self._sceneviewer.getScene()
            graphics_filter = self._sceneviewer.getScenefilter()
            self._scenepicker = scene.createScenepicker()
            region = scene.getRegion()

            fieldmodule = region.getFieldmodule()

            self._selectionGroup = fieldmodule.createFieldGroup()
            scene.setSelectionField(self._selectionGroup)

            self._scenepicker = scene.createScenepicker()
            self._scenepicker.setScenefilter(graphics_filter)
            sceneFilterModule = self.getContext().getScenefiltermodule()
            self._sceneSurfacesFilter = sceneFilterModule.createScenefilterOperatorAnd()
            surfacesFilter = sceneFilterModule.createScenefilterGraphicsType(Graphics.TYPE_SURFACES)
            self._sceneSurfacesFilter.appendOperand(graphics_filter)
            self._sceneSurfacesFilter.appendOperand(surfacesFilter)
            self.createSelectionBox(scene)            
        
    def setNodeSelection(self, enabled):
        self._nodeSelectMode = enabled
        self.selectionSettingsChanged.emit()
        
    def setSelectionModeAdditive(self):
        self._selectionAlwaysAdditive = True
        
    def setLineSelection(self, enabled):
        self._1delemSelectMode = enabled
        
    def setSurfacesSelection(self, enabled):
        self._2delemSelectMode = enabled
        
    def setElementSelection(self, enabled):
        self._elemSelectMode = enabled
        self.selectionSettingsChanged.emit()
        
    def enableSelectionToggle(self):
        self.setNodeSelection(self.ui.enableSelection.isChecked())
        
    def elementSelectionToggle(self):
        self.setElementSelection(self.ui.elementSelection.isChecked())
    
    def lineSelectionToggle(self):
        self.setLineSelection(self.ui.linesSelection.isChecked())
            
    def surfacesSelectionToggle(self):
        self.setSurfacesSelection(self.ui.surfacesSelection.isChecked())

    def setSelectModeAll(self):
        self._nodeSelectMode = True
        self._dataSelectMode = True
        self._elemSelectMode = True
        
    def createSelectionBox(self, scene):
        if self._selection_box:
            previousScene = self._selection_box.getScene()
            previousScene.removeGraphics(self._selection_box)
        
        self._selection_box = scene.createGraphicsPoints()
        self._selection_box.setName(SELECTION_RUBBERBAND_NAME)
        self._selection_box.setScenecoordinatesystem(SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT)
        
        attributes = self._selection_box.getGraphicspointattributes()
        attributes.setGlyphShapeType(Glyph.SHAPE_TYPE_CUBE_WIREFRAME)
        attributes.setBaseSize([10, 10, 0.9999])
        attributes.setGlyphOffset([1, -1, 0])
        self._selection_box.setBaseSize = attributes.setBaseSize
        self._selection_box._setGlyphOffset = attributes.setGlyphOffset   
        self._selection_box.setVisibilityFlag(False)
    
    def getScenepicker(self):
        return self._scenepicker

    def setPickingRectangle(self, coordinate_system, left, bottom, right, top):
        self._scenepicker.setSceneviewerRectangle(self._sceneviewer, coordinate_system, left, bottom, right, top);

    def setSelectionfilter(self, scenefilter):
        self._scenepicker.setScenefilter(scenefilter)

    def getSelectionfilter(self):
        result, scenefilter = self._scenepicker.getScenefilter()
        if result == OK:
            return scenefilter
        return None
            
    def _getNearestGraphic(self, x, y, domain_type):
        self._scenepicker.setSceneviewerRectangle(self._sceneviewer, SCENECOORDINATESYSTEM_LOCAL, x - 0.5, y - 0.5, x + 0.5, y + 0.5)
        nearest_graphics = self._scenepicker.getNearestGraphics()
        if nearest_graphics.isValid() and nearest_graphics.getFieldDomainType() == domain_type:
            return nearest_graphics

        return None

    def getNeareshGraphics(self):
        return self._scenepicker.getNearestGraphics()

    def getNearestGraphicsNode(self, x, y):
        return self._getNearestGraphic(x, y, Field.DOMAIN_TYPE_NODES)

    def getNearestGraphicsPoint(self, x, y):
        '''
        Assuming given x and y is in the sending widgets coordinates 
        which is a parent of this widget.  For example the values given 
        directly from the event in the parent widget.
        '''
        return self._getNearestGraphic(x, y, Field.DOMAIN_TYPE_POINT)

    def getNearestNode(self, x, y):
        self._scenepicker.setSceneviewerRectangle(self._sceneviewer, SCENECOORDINATESYSTEM_LOCAL, x - 0.5, y - 0.5, x + 0.5, y + 0.5)
        node = self._scenepicker.getNearestNode()

        return node

    def setScenefilter(self, scenefilter):
        self._scenepicker.setScenefilter(scenefilter)
        SceneviewerWidget.setScenefilter(self, scenefilter)

    def addPickedNodesToFieldGroup(self, selection_group):
        self._scenepicker.addPickedNodesToFieldGroup(selection_group)
        
    def elementConstrainFunction(self, fieldmodule, fieldcache, coordinates, elementCoordinateField, meshGroup):
        '''
        Return new coordinates which is constrained to the meshGroup
        '''
        fieldLocation = fieldmodule.createFieldFindMeshLocation(elementCoordinateField, \
                            elementCoordinateField, meshGroup)
        fieldLocation.setSearchMode(FieldFindMeshLocation.SEARCH_MODE_NEAREST)
        fieldcache.setFieldReal(elementCoordinateField, coordinates)
        element, chartCoordinates = fieldLocation.evaluateMeshLocation(fieldcache, 3)
        fieldcache.setMeshLocation(element, chartCoordinates)
        return_code, newCoordinates = elementCoordinateField.evaluateReal(fieldcache, 3)
        return True, newCoordinates

    def nodeIsSelectedAtCoordinates(self, x, y):
        '''
        Return node and its coordinates field if its valid
        '''
        self._scenepicker.setSceneviewerRectangle(self._sceneviewer, SCENECOORDINATESYSTEM_LOCAL, \
                                                  x - 3, y - 3, \
                                                  x + 3, y + 3);
        node = self._scenepicker.getNearestNode()
        if node.isValid():
            nodeset = node.getNodeset()
            nodegroup = self._selectionGroup.getFieldNodeGroup(nodeset)
            if nodegroup.isValid():
                group = nodegroup.getNodesetGroup()
                if group.containsNode(node):
                    graphics = self._scenepicker.getNearestGraphics()
                    if graphics.getFieldDomainType() == Field.DOMAIN_TYPE_NODES:
                        return True, node, graphics.getCoordinateField(), graphics
        return False, None, None, None
    
    
    def getNearestSurfacesElementAndCoordinates(self, x, y):
        '''
        Return element and its coordinates field if its valid
        '''
        self._scenepicker.setSceneviewerRectangle(self._sceneviewer, SCENECOORDINATESYSTEM_LOCAL, \
                                                  x - 3, y - 3, x + 3, y + 3)
        nearestGraphics = self._scenepicker.getNearestGraphics()
        if nearestGraphics.isValid():
            surfacesGraphics = nearestGraphics.castSurfaces()
            if surfacesGraphics.isValid():
                nearestElement = self._scenepicker.getNearestElement()
                elementCoordinateField = surfacesGraphics.getCoordinateField()
                return True, nearestElement, elementCoordinateField
        return False, None, None
        
    def mousePressEvent(self, event):
        '''
        Inform the scene viewer of a mouse press event.
        '''
        event.accept()
        self._handle_mouse_events = False  # Track when the zinc should be handling mouse events
        if not self._ignore_mouse_events and (event.modifiers() & self._selectionModifier) and (self._nodeSelectMode or self._elemSelectMode) and button_map[event.button()] == Sceneviewerinput.BUTTON_TYPE_LEFT:
            self._selection_position_start = (event.x(), event.y())
            self._selection_mode = SelectionMode.EXCLUSIVE
            if event.modifiers() & self._additiveSelectionModifier:
                self._selection_mode = SelectionMode.ADDITIVE
        elif not self._ignore_mouse_events and not event.modifiers() or (event.modifiers() & self._selectionModifier and button_map[event.button()] == Sceneviewerinput.BUTTON_TYPE_RIGHT):
            SceneviewerWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        '''
        Inform the scene viewer of a mouse release event.
        '''
        event.accept()
        if not self._ignore_mouse_events and self._selection_mode != SelectionMode.NONE:
            x = event.x()
            y = event.y()
            # Construct a small frustum to look for nodes in.
            top_region = self._sceneviewer.getScene().getRegion()
            top_region.beginHierarchicalChange()
            self._selection_box.setVisibilityFlag(False)
            if (x != self._selection_position_start[0] and y != self._selection_position_start[1]):
                left = min(x, self._selection_position_start[0])
                right = max(x, self._selection_position_start[0])
                bottom = min(y, self._selection_position_start[1])
                top = max(y, self._selection_position_start[1])
                self._scenepicker.setSceneviewerRectangle(self._sceneviewer, SCENECOORDINATESYSTEM_LOCAL, left, bottom, right, top);
                if self._selection_mode == SelectionMode.EXCLUSIVE:
                    self._selectionGroup.clear()
                if self._nodeSelectMode or self._dataSelectMode:
                    self._scenepicker.addPickedNodesToFieldGroup(self._selectionGroup)
                if self._elemSelectMode:
                    self._scenepicker.addPickedElementsToFieldGroup(self._selectionGroup)
            else:
                self._scenepicker.setSceneviewerRectangle(self._sceneviewer, SCENECOORDINATESYSTEM_LOCAL, x - 3.5, y - 3.5, x + 3.5, y + 3.5)
                if self._nodeSelectMode and self._elemSelectMode and self._selection_mode == SelectionMode.EXCLUSIVE and not self._scenepicker.getNearestGraphics().isValid():
                    self._selectionGroup.clear()

                if self._nodeSelectMode and (self._scenepicker.getNearestGraphics().getFieldDomainType() == Field.DOMAIN_TYPE_NODES):
                    node = self._scenepicker.getNearestNode()
                    nodeset = node.getNodeset()
                    nodegroup = self._selectionGroup.getFieldNodeGroup(nodeset)
                    if not nodegroup.isValid():
                        nodegroup = self._selectionGroup.createFieldNodeGroup(nodeset)
                    group = nodegroup.getNodesetGroup()
                    if self._selection_mode == SelectionMode.EXCLUSIVE:
                        remove_current = group.getSize() == 1 and group.containsNode(node)
                        self._selectionGroup.clear()
                        if not remove_current:
                            group.addNode(node)
                    elif self._selection_mode == SelectionMode.ADDITIVE:
                        if group.containsNode(node):
                            group.removeNode(node)
                        else:
                            group.addNode(node)
                if self._elemSelectMode and (self._scenepicker.getNearestGraphics().getFieldDomainType() in [Field.DOMAIN_TYPE_MESH1D, Field.DOMAIN_TYPE_MESH2D, Field.DOMAIN_TYPE_MESH3D, Field.DOMAIN_TYPE_MESH_HIGHEST_DIMENSION]):
                    elem = self._scenepicker.getNearestElement()
                    mesh = elem.getMesh()
                    elementgroup = self._selectionGroup.getFieldElementGroup(mesh)
                    if not elementgroup.isValid():
                        elementgroup = self._selectionGroup.createFieldElementGroup(mesh)
                    group = elementgroup.getMeshGroup()
                    if self._selection_mode == SelectionMode.EXCLUSIVE:
                        remove_current = group.getSize() == 1 and group.containsElement(elem)
                        self._selectionGroup.clear()
                        if not remove_current:
                            group.addElement(elem)
                    elif self._selection_mode == SelectionMode.ADDITIVE:
                        if group.containsElement(elem):
                            group.removeElement(elem)
                        else:
                            group.addElement(elem)
            top_region.endHierarchicalChange()
            self._selection_mode = SelectionMode.NONE
        elif not self._ignore_mouse_events and self._handle_mouse_events:
            SceneviewerWidget.mouseReleaseEvent(self, event)
        self._selection_mode = SelectionMode.NONE

    def mouseMoveEvent(self, event):
        '''
        Inform the scene viewer of a mouse move event and update the OpenGL scene to reflect this
        change to the viewport.
        '''
        event.accept()
        if not self._ignore_mouse_events and self._selection_mode != SelectionMode.NONE:
            x = event.x()
            y = event.y()
            xdiff = float(x - self._selection_position_start[0])
            ydiff = float(y - self._selection_position_start[1])
            if abs(xdiff) < 0.0001:
                xdiff = 1
            if abs(ydiff) < 0.0001:
                ydiff = 1
            xoff = float(self._selection_position_start[0]) / xdiff + 0.5
            yoff = float(self._selection_position_start[1]) / ydiff + 0.5
            scene = self._selection_box.getScene()
            scene.beginChange()
            attributes = self._selection_box.getGraphicspointattributes()
            attributes.setBaseSize([xdiff, ydiff, 0.999])
            attributes.setGlyphOffset([xoff, -yoff, 0])
            self._selection_box.setVisibilityFlag(True)
            scene.endChange()
        elif not self._ignore_mouse_events and self._handle_mouse_events:
            SceneviewerWidget.mouseMoveEvent(self, event)

