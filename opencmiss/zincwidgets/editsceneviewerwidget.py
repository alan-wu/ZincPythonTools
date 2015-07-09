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
    
from selectionsceneviewerwidget import SelectionSceneviewerWidget, SelectionMode
from opencmiss.zinc.sceneviewer import Sceneviewer, Sceneviewerevent
from opencmiss.zinc.graphics import Graphics
from opencmiss.zinc.sceneviewerinput import Sceneviewerinput
from sceneviewerwidget import button_map, modifier_map
from opencmiss.zinc.scenepicker import Scenepicker
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.scenecoordinatesystem import \
        SCENECOORDINATESYSTEM_LOCAL, \
        SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT,\
        SCENECOORDINATESYSTEM_WORLD
from opencmiss.zinc.field import Field, FieldFindMeshLocation
import math
from editsceneviewerwidget_ui import Ui_EditSceneviewerWidget

class NodeEditInfo():
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._node = None
        self._graphics = None
        self._coordinateField = None
        self._orientationField = None
        self._glyphCentre = [0.0, 0.0, 0.0]
        self._glyphSize = [0.0, 0.0, 0.0]
        self._glyphScaleFactors = [0.0, 0.0, 0.0]
        self._variableScaleField = Field()        
        self._nearestElement = None
        self._elementCoordinateField = None
        self._createCoordinatesField = None

class EditSceneviewerWidget(SelectionSceneviewerWidget):

    def __init__(self, parent=None, shared=None):
        
        # Selection attributes
        SelectionSceneviewerWidget.__init__(self, parent, shared)
        self._nodeEditMode = False
        self._nodeEditVectorMode = False
        self._nodeCreateMode = False
        self._nodeConstrainMode = False
        self._ignore_mouse_events = False
        self._editModifier = QtCore.Qt.CTRL
        self._nodeEditInfo = NodeEditInfo()
        self._createCoordinatesField = None
        
    def setEditModifier(self, modifierIn):
        self._editModifier = modifierIn
        
    def setNodeEdit(self, enabled):
        self._nodeEditMode = enabled
        self.selectionSettingsChanged.emit()
        
    def setNodeConstrainToSurfacesMode(self, enabled):
        self._nodeConstrainMode = enabled
        self.selectionSettingsChanged.emit()

    def setNodeCreateMode(self, enabled):
        self._nodeCreateMode = enabled
        self.selectionSettingsChanged.emit()
        
    def setNodeCreateCoordinatesField(self, coordinatesField):
        self._createCoordinatesField = coordinatesField
        
    def createCoordinatesVectorsGraphics(self, scene, coordinateField, valueLabel, \
                                             versionNumber, baseSizes, scaleFactors, selectMode, \
                                             material, selectedMaterial):
        '''
        Create graphics for the vector of the supplied scene which allow the vector to be edited. 
        '''
        fieldmodule = scene.getRegion().getFieldmodule()
        derivativeField =  fieldmodule.createFieldNodeValue(coordinateField, valueLabel, versionNumber)
        if derivativeField.isValid():
            nodes = scene.createGraphicsPoints()
            nodes.setCoordinateField(coordinateField)
            nodes.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
            nodes.setSelectMode(selectMode)
            nodes.setMaterial(material)
            nodes.setSelectedMaterial(selectedMaterial)
            attributes = nodes.getGraphicspointattributes()
            attributes.setGlyphShapeType(Glyph.SHAPE_TYPE_ARROW_SOLID)
            attributes.setBaseSize(baseSizes)
            attributes.setScaleFactors(scaleFactors)
            attributes.setOrientationScaleField(derivativeField)
            #gfx modify g_element bicubic_linear node_points coordinate coordinates glyph arrow_solid size "0*0.1*0.1" scale_factors "0.5*0*0" orientation dx_ds1 mat gold selected_mat gold draw_selected
        return None
    
    def makeGlyphOrientationScaleAxes(self, orientationScaleValues):
        num = len(orientationScaleValues)
        size = [0.0, 0.0, 0.0]
        axis1 = [0.0, 0.0, 0.0]
        axis2 = [0.0, 0.0, 0.0]
        axis3 = [0.0, 0.0, 0.0]
        if num == 0:
            size = [0.0, 0.0, 0.0]
            axis1 = [1.0, 0.0, 0.0]
            axis2 = [0.0, 1.0, 0.0]
            axis3 = [0.0, 0.0, 1.0]
        elif num == 1:
            size = [orientationScaleValues[0], orientationScaleValues[1],orientationScaleValues[2]];
            axis1 = [1.0, 0.0, 0.0]
            axis2 = [0.0, 1.0, 0.0]
            axis3 = [0.0, 0.0, 1.0]
        elif num == 2:
            axis1 = [orientationScaleValues[0], orientationScaleValues[1], 0.0]
            magnitude = math.sqrt(axis1[0]*axis1[0]+axis1[1]*axis1[1])
            if magnitude > 0.0:
                axis1[0] /= magnitude
                axis1[1] /= magnitude                
            size = [magnitude, magnitude, magnitude] 
            axis2 = [-axis1[1], axis1[0], 0.0]
            axis3 = [0.0, 0.0, 1.0];
        elif num == 3:
            axis1 = orientationScaleValues
            magnitude = math.sqrt(axis1[0]*axis1[0]+axis1[1]*axis1[1]+axis1[2]*axis1[2])
            if magnitude > 0.0:
                axis1[0] /= magnitude
                axis1[1] /= magnitude
                axis1[2] /= magnitude 
                size = [magnitude, magnitude, magnitude]
                axis3 = [0.0, 0.0, 0.0]
                if math.fabs(axis1[0]) < math.fabs(axis1[1]):
                    if math.fabs(axis1[2]) < math.fabs(axis1[0]):
                        axis3[2]=1.0
                    else:
                        axis3[0]=1.0
                else:
                    if math.fabs(axis1[2]) < math.fabs(axis1[1]):
                        axis3[2]=1.0
                    else:
                        axis3[1]=1.0
                axis2[0]=axis3[1]*axis1[2]-axis3[2]*axis1[1]
                axis2[1]=axis3[2]*axis1[0]-axis3[0]*axis1[2]
                axis2[2]=axis3[0]*axis1[1]-axis3[1]*axis1[0]
                magnitude=math.sqrt(axis2[0]*axis2[0]+axis2[1]*axis2[1]+axis2[2]*axis2[2])
                axis2[0] /= magnitude
                axis2[1] /= magnitude
                axis2[2] /= magnitude
                axis3[0]=axis1[1]*axis2[2]-axis1[2]*axis2[1]
                axis3[1]=axis1[2]*axis2[0]-axis1[0]*axis2[2]
                axis3[2]=axis1[0]*axis2[1]-axis1[1]*axis2[0]
            else:
                axis2=[0.0, 0.0, 0.0]
                axis3=[0.0, 0.0, 0.0]
                size=[0.0, 0.0, 0.0]
        elif num == 4 or num == 6:
            if num == 4:
                axis1 = [orientationScaleValues[0], orientationScaleValues[1], 0.0]
                axis2 = [orientationScaleValues[2], orientationScaleValues[3], 0.0]
            else:
                axis1 = [orientationScaleValues[0], orientationScaleValues[1], orientationScaleValues[2]]
                axis2 = [orientationScaleValues[3], orientationScaleValues[4], orientationScaleValues[5]]
            axis3[0]=axis1[1]*axis2[2]-axis1[2]*axis2[1]
            axis3[1]=axis1[2]*axis2[0]-axis1[0]*axis2[2]
            axis3[2]=axis1[0]*axis2[1]-axis1[1]*axis2[0]
            magnitude=math.sqrt(axis1[0]*axis1[0]+axis1[1]*axis1[1]+axis1[2]*axis1[2])
            if magnitude > 0.0:
                axis1[0] /= magnitude
                axis1[1] /= magnitude
                axis1[2] /= magnitude
            size[0]=magnitude;
            magnitude=math.sqrt(axis2[0]*axis2[0]+axis2[1]*axis2[1]+axis2[2]*axis2[2])
            if magnitude > 0.0:
                axis2[0] /= magnitude
                axis2[1] /= magnitude
                axis2[2] /= magnitude
            size[1]=magnitude;
            magnitude=math.sqrt(axis3[0]*axis3[0]+axis3[1]*axis3[1]+axis3[2]*axis3[2])
            if magnitude > 0.0:
                axis3[0] /= magnitude
                axis3[1] /= magnitude
                axis3[2] /= magnitude
            size[2]=magnitude;
        elif num == 9:
            axis1=[orientationScaleValues[0],orientationScaleValues[1],orientationScaleValues[2]]
            magnitude=math.sqrt(axis1[0]*axis1[0]+axis1[1]*axis1[1]+axis1[2]*axis1[2])
            if magnitude > 0.0:
                axis1[0] /= magnitude
                axis1[1] /= magnitude
                axis1[2] /= magnitude   
            size[0]=magnitude;
            axis2=[orientationScaleValues[3],orientationScaleValues[4],orientationScaleValues[5]]
            magnitude=math.sqrt(axis2[0]*axis2[0]+axis2[1]*axis2[1]+axis2[2]*axis2[2])
            if magnitude > 0.0:
                axis2[0] /= magnitude
                axis2[1] /= magnitude
                axis2[2] /= magnitude   
            size[1]=magnitude
            axis3=[orientationScaleValues[6],orientationScaleValues[7],orientationScaleValues[8]]
            magnitude=math.sqrt(axis3[0]*axis3[0]+axis3[1]*axis3[1]+axis3[2]*axis3[2])
            if magnitude > 0.0:
                axis3[0] /= magnitude
                axis3[1] /= magnitude
                axis3[2] /= magnitude  
            size[2]=magnitude;
        return axis1, axis2, axis3, size
 
    def getVectorDelta(self, nodeEditInfo, x, y):
        '''
        Get the delta of position between selected nodes and provided windows coordinates
        '''
        delta = [0.0, 0.0, 0.0]
        fieldmodule = nodeEditInfo._node.getNodeset().getFieldmodule()
        fieldcache = fieldmodule.createFieldcache()
        fieldcache.setNode(nodeEditInfo._node)
        numberOfComponents = nodeEditInfo._orientationField.getNumberOfComponents()
        
        if numberOfComponents > 0 and numberOfComponents <= 9 and nodeEditInfo._orientationField.isValid() and \
            nodeEditInfo._coordinateField.isValid() and nodeEditInfo._glyphScaleFactors[0] != 0.0 and \
            nodeEditInfo._glyphCentre[0] == 0.0 and nodeEditInfo._glyphSize[0] == 0.0 and \
            False == nodeEditInfo._variableScaleField.isValid():
            return_code, orientation = nodeEditInfo._orientationField.evaluateReal(fieldcache, numberOfComponents)
            return_code, coordinates = nodeEditInfo._coordinateField.evaluateReal(fieldcache, 3)
            axis1, axis2, axis3, num = self.makeGlyphOrientationScaleAxes(orientation)
            oldCoordinates = [coordinates[0], coordinates[1], coordinates[2]]
            endCoordinates = [0.0, 0.0, 0.0]
            endCoordinates[0] = coordinates[0]+nodeEditInfo._glyphSize[0]*nodeEditInfo._glyphScaleFactors[0]*axis1[0];
            endCoordinates[1] = coordinates[1]+nodeEditInfo._glyphSize[0]*nodeEditInfo._glyphScaleFactors[0]*axis1[1];
            endCoordinates[2] = coordinates[2]+nodeEditInfo._glyphSize[0]*nodeEditInfo._glyphScaleFactors[0]*axis1[2];
            projectCoordinates = self.project(endCoordinates[0], endCoordinates[1], endCoordinates[2])
            endCoordinates = self.unproject(x, y * -1.0, projectCoordinates[2])
            a = [0.0, 0.0, 0.0]
            a[0]=(endCoordinates[0]-oldCoordinates[0])/nodeEditInfo._glyphScaleFactors[0]
            a[1]=(endCoordinates[1]-oldCoordinates[1])/nodeEditInfo._glyphScaleFactors[0]
            a[2]=(endCoordinates[2]-oldCoordinates[2])/nodeEditInfo._glyphScaleFactors[0]
            if numberOfComponents == 1:
                delta[0] = a[0]
            elif numberOfComponents == 2 or numberOfComponents == 4:
                delta[0] = a[0]
                delta[1] = a[1]
            elif numberOfComponents == 3 or numberOfComponents == 6 or numberOfComponents == 9:
                delta[0] = a[0]
                delta[1] = a[1]
                delta[2] = a[2]

        return delta
    
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
    
    def getPlacementPoint(self, nodeEditInfo, x, y):
        '''
        Return the world coordinates with the informations provided in nodeEditInfo
        '''
        if not nodeEditInfo._nearestElement:
            if nodeEditInfo._node and nodeEditInfo._node.isValid():
                fieldmodule = nodeEditInfo._node.getNodeset().getFieldmodule()
                fieldcache = fieldmodule.createFieldcache()
                fieldcache.setNode(nodeEditInfo._node)
                return_code, coordinates = nodeEditInfo._coordinateField.evaluateReal(fieldcache, 3)
                projectCoordinates = self.project(coordinates[0], coordinates[1], coordinates[2])
                unprojectCoordinates = self.unproject(x, y * -1.0, projectCoordinates[2])
                return True, unprojectCoordinates
            else:
                return self._scenepicker.getPickingVolumeCentre()
        else:
            fieldmodule = nodeEditInfo._nearestElement.getMesh().getFieldmodule()
            fieldcache = fieldmodule.createFieldcache()
            converged = False
            fieldcache.setMeshLocation(nodeEditInfo._nearestElement, [0.5, 0.5, 0.5])
            temp, unprojectCoordinates = self._scenepicker.getPickingVolumeCentre()
            fieldcache.clearLocation()
            mesh = nodeEditInfo._nearestElement.getMesh()
            fieldmodule = nodeEditInfo._elementCoordinateField.getFieldmodule()
            meshGroup = fieldmodule.createFieldGroup().createFieldElementGroup(mesh).getMeshGroup()
            meshGroup.addElement(nodeEditInfo._nearestElement)
            return_code = True 
            steps = 0
            point = unprojectCoordinates
            while return_code == True and converged == False:
                previous_point = point
                temp, fe_value_point = self.elementConstrainFunction(fieldmodule, fieldcache, \
                                                                     previous_point, \
                                                                     nodeEditInfo._elementCoordinateField, \
                                                                     meshGroup)
                changes = [point[0] - fe_value_point[0], point[1] - fe_value_point[1], \
                           point[2] - fe_value_point[2]]
                if math.sqrt(changes[0]*changes[0] + changes[1]*changes[1] + changes[2]*changes[2]) < 1.0e-4:
                    converged = True
                else:
                    point[0] = fe_value_point[0];
                    point[1] = fe_value_point[1];
                    point[2] = fe_value_point[2];
                    steps = steps + 1
                    if steps > 1000:
                        return_code = False
                    projectCoordinates = self.project(point[0], point[1], point[2])
                    point = self.unproject(x * 1.0, y * -1.0, projectCoordinates[2])
                    changes = [point[0] - previous_point[0], point[1] - previous_point[1], 
                                        point[2] - previous_point[2]]
                    if math.sqrt(changes[0]*changes[0] + changes[1]*changes[1] + changes[2]*changes[2]) < 1.0e-6:
                        return_code = False
            return True, point
        
    def getCoordinatesDelta(self, nodeEditInfo, x, y):
        '''
        Get the delta of position between selected nodes and provided windows coordinates
        '''
        fieldmodule = nodeEditInfo._node.getNodeset().getFieldmodule()
        fieldcache = fieldmodule.createFieldcache()
        fieldcache.setNode(nodeEditInfo._node)
        delta = [0.0, 0.0, 0.0]
        return_code, coordinates = nodeEditInfo._coordinateField.evaluateReal(fieldcache, 3)
        return_code, newCoordinates = self.getPlacementPoint(nodeEditInfo, x, y)
        if return_code:
            delta = [newCoordinates[0] - coordinates[0],  newCoordinates[1] - coordinates[1],\
                     newCoordinates[2] - coordinates[2]]
        return delta
    
    def updateNodePositionWithDelta(self, fieldcache, coordinateField, node, xdiff, ydiff, zdiff):
        '''
        Updated coordinates of a single node with delta
        '''
        fieldcache.setNode(node)
        return_code, coordinates = coordinateField.evaluateReal(fieldcache, 3)
        coordinateField.assignReal(fieldcache, [coordinates[0]+xdiff, \
                                                coordinates[1]+ydiff, \
                                                coordinates[2]+zdiff])
#    def updateSelectedNodesInRegionWithDelta(self, region, xdiff, ydiff, zdiff):
#        childRegion = region.getFirstChild()
#        while childRegion.isValid():
#            updateSelectedNodesInRegion(self, childRegion, xdiff, ydiff, zdiff)
#            childRegion = childRegion.getNextSibling()
#        nodeset = region.getFieldmodule().findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
#        if nodeset.isValid():
#            nodegroup = self._selectionGroup.getFieldNodeGroup(nodeset)
#            if nodegroup.isValid():
#                nodesetgroup = nodegroup.getNodesetGroup()
#                if nodesetgroup.isValid():
#                    iterator = nodesetgroup.createNodeiterator()
#                    node = iterator.next()
#                    while node.isValid():                        
#                        node = iterator.next()
            
    def updateSelectedNodesCoordinatesWithDelta(self, nodeEditInfo, selectionGroup, xdiff, ydiff, zdiff):
        '''
        Updated nodes in the selection group with delta
        '''
        nodegroup = selectionGroup.getFieldNodeGroup(nodeEditInfo._node.getNodeset())
        if nodegroup.isValid():
            group = nodegroup.getNodesetGroup()
            if group.isValid():
                fieldmodule = nodegroup.getFieldmodule()
                fieldmodule.beginChange()
                fieldcahce = fieldmodule.createFieldcache()
                iterator = group.createNodeiterator()
                node = iterator.next()
                while node.isValid():            
                    self.updateNodePositionWithDelta(fieldcahce, nodeEditInfo._coordinateField, \
                                                     node, xdiff, ydiff, zdiff)            
                    node = iterator.next()
                fieldmodule.endChange()
                
    def updateNodeVectorWithDelta(self, fieldcache, orientationField, node, xdiff, ydiff, zdiff):
        '''
        Updated the orientation field of a node with delta
        '''
        fieldcache.setNode(node)
        numberOfComponents = orientationField.getNumberOfComponents()
        return_code, orientationScale = orientationField.evaluateReal(fieldcache, numberOfComponents)
        if numberOfComponents == 1:
            orientationScale[0] = xdiff
        elif numberOfComponents == 2 or numberOfComponents == 4:
            orientationScale[0] = xdiff
            orientationScale[1] = ydiff
        elif numberOfComponents == 3 or numberOfComponents == 6 or numberOfComponents == 9:
            orientationScale[0] = xdiff
            orientationScale[1] = ydiff
            orientationScale[2] = zdiff
        orientationField.assignReal(fieldcache, orientationScale)
                
    def updateSelectedNodesVectorWithDelta(self, nodeEditInfo, selectionGroup, xdiff, ydiff, zdiff):
        '''
        Updated orientation field provided at nodes in the selection group with delta
        '''
        nodegroup = selectionGroup.getFieldNodeGroup(nodeEditInfo._node.getNodeset())
        if nodegroup.isValid():
            group = nodegroup.getNodesetGroup()
            if group.isValid():
                fieldmodule = nodegroup.getFieldmodule()
                fieldmodule.beginChange()
                fieldcahce = fieldmodule.createFieldcache()
                iterator = group.createNodeiterator()
                node = iterator.next()
                while node.isValid():            
                    self.updateNodeVectorWithDelta(fieldcahce, nodeEditInfo._orientationField, \
                                                     node, xdiff, ydiff, zdiff)            
                    node = iterator.next()
                fieldmodule.endChange()
                
    def createNodeAtCoordinates(self, nodeEditInfo, x, y):
        '''
        Create a new node at a location based on information provided by nodeEditInfo 
        '''
        return_code, newCoordinates = self.getPlacementPoint(nodeEditInfo, x, y)
        if nodeEditInfo._createCoordinatesField and nodeEditInfo._createCoordinatesField.isValid():
            fieldmodule = nodeEditInfo._createCoordinatesField.getFieldmodule()
            fieldmodule.beginChange()
            nodeset = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
            nodetemplate = nodeset.createNodetemplate()
            nodetemplate.defineField(nodeEditInfo._createCoordinatesField)
            node = nodeset.createNode(-1, nodetemplate)
            fieldcache = fieldmodule.createFieldcache()
            fieldcache.setNode(node)
            nodeEditInfo._createCoordinatesField.assignReal(fieldcache, newCoordinates)
            fieldmodule.endChange()
            
    def mousePressEvent(self, event):
        '''
        Inform the scene viewer of a mouse press event.
        '''
        self._handle_mouse_events = False  # Track when the zinc should be handling mouse events
        if not self._ignore_mouse_events and (event.modifiers() & self._editModifier) and \
            (self._nodeEditMode or self._nodeEditVectorMode or self._nodeCreateMode) and \
            button_map[event.button()] == Sceneviewerinput.BUTTON_TYPE_LEFT:
            return_code, selectedNode, selectedCoordinateField, selectedGraphics = \
                self.nodeIsSelectedAtCoordinates(event.x(), event.y())
            if return_code:
                self._nodeEditInfo._node = selectedNode
                self._nodeEditInfo._coordinateField = selectedCoordinateField
                self._nodeEditInfo._graphics = selectedGraphics
                self._selection_position_start = (event.x(), event.y())
                if self._nodeEditMode:
                    self._selection_mode = SelectionMode.EDIT_POSITION
                else:
                    attributes = self._nodeEditInfo._graphics.getGraphicspointattributes()
                    if attributes.isValid():
                        self._nodeEditInfo._orientationField = attributes.getOrientationScaleField()
                        if self._nodeEditInfo._orientationField and self._nodeEditInfo._orientationField.isValid():
                            self._selection_mode = SelectionMode.EDIT_VECTOR
                            return_code, self._nodeEditInfo._glyphCentre = attributes.getGlyphOffset(3)
                            return_code, self._nodeEditInfo._glyphSize = attributes.getBaseSize(3)
                            return_code, self._nodeEditInfo._glyphScaleFactors = attributes.getScaleFactors(3)
                            self._nodeEditInfo._variableScaleField = attributes.getSignedScaleField()
            elif self._nodeCreateMode:
                self._selection_mode = SelectionMode.CREATE
        else:
            SelectionSceneviewerWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        '''
        Inform the scene viewer of a mouse release event.
        '''
        if not self._ignore_mouse_events and (self._selection_mode == SelectionMode.EDIT_POSITION or \
                                              self._selection_mode == SelectionMode.EDIT_VECTOR):
            self._nodeEditInfo.reset()
        elif not self._ignore_mouse_events and self._selection_mode == SelectionMode.CREATE:
            x = event.x()
            y = event.y()
            self._selection_box.setVisibilityFlag(False)
            if self._createCoordinatesField and self._createCoordinatesField.isValid():
                self._nodeEditInfo._createCoordinatesField = self._createCoordinatesField
                if self._nodeConstrainMode == True:
                    returnCode, self._nodeEditInfo._nearestElement, self._nodeEditInfo._elementCoordinateField = \
                        self.getNearestSurfacesElementAndCoordinates(x, y)
                    if self._nodeEditInfo._nearestElement and self._nodeEditInfo._elementCoordinateField:
                        self.createNodeAtCoordinates(self._nodeEditInfo, x, y)   
                else:
                    self.createNodeAtCoordinates(self._nodeEditInfo, x, y)
            self._nodeEditInfo.reset()
        else:
            SelectionSceneviewerWidget.mouseReleaseEvent(self, event)
        self._selection_mode = SelectionMode.NONE

    def mouseMoveEvent(self, event):
        '''
        Inform the scene viewer of a mouse move event and update the OpenGL scene to reflect this
        change to the viewport.
        '''
        
        if not self._ignore_mouse_events and self._selection_mode != SelectionMode.NONE:
            x = event.x()
            y = event.y()
            xdiff = float(x - self._selection_position_start[0])
            ydiff = float(y - self._selection_position_start[1])
            if abs(xdiff) < 0.0001:
                xdiff = 1
            if abs(ydiff) < 0.0001:
                ydiff = 1            
            if self._selection_mode == SelectionMode.EDIT_POSITION:
                if self._nodeConstrainMode == True:
                    returnCode, self._nodeEditInfo._nearestElement, self._nodeEditInfo._elementCoordinateField = \
                        self.getNearestSurfacesElementAndCoordinates(x, y)
                    if self._nodeEditInfo._nearestElement and self._nodeEditInfo._elementCoordinateField:
                        delta = self.getCoordinatesDelta(self._nodeEditInfo, x, y)
                        self.updateSelectedNodesCoordinatesWithDelta(self._nodeEditInfo, \
                            self._selectionGroup, delta[0], delta[1], delta[2])                
                else:
                    delta = self.getCoordinatesDelta(self._nodeEditInfo, x, y)
                    self.updateSelectedNodesCoordinatesWithDelta(self._nodeEditInfo, \
                            self._selectionGroup, delta[0], delta[1], delta[2])
            elif self._selection_mode == SelectionMode.EDIT_VECTOR:
                if self._nodeEditInfo._orientationField and self._nodeEditInfo._orientationField.isValid():
                    delta = self.getVectorDelta(self._nodeEditInfo, x, y)
                    self.updateSelectedNodesVectorWithDelta(self._nodeEditInfo, \
                            self._selectionGroup, delta[0], delta[1], delta[2])
            else:
                SelectionSceneviewerWidget.mouseMoveEvent(self, event)
        elif not self._ignore_mouse_events and self._handle_mouse_events:
            SelectionSceneviewerWidget.mouseMoveEvent(self, event)
        