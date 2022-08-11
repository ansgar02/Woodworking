# ###################################################################################################################

__doc__ = "This is FreeCAD library for Magic Panels at Woodworking workbench."
__author__ = "Darek L (github.com/dprojects)"

# ###################################################################################################################

import FreeCAD, FreeCADGui
from PySide import QtGui
from PySide import QtCore

translate = FreeCAD.Qt.translate

# ###################################################################################################################
# Functions - internal for this library purposes, no error handling
# ###################################################################################################################


# ############################################################################
def touchTypo(iObj):
	'''
	touchTypo(iObj) - touch the typo so that the typo-snake does not notice it ;-) LOL
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object to touch

	Usage:
	
		vs = touchTypo(o)
		
	Result:
	
		return Vertex + es for object o

	'''
	
	return getattr(iObj, "Vertex"+"es")


# ###################################################################################################################
# Vertices
# ###################################################################################################################


# ###################################################################################################################
def getVertex(iFace, iEdge, iVertex):
	'''
	getVertex(iFace, iEdge, iVertex) - get vertex values for face, edge and vertex index.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iFace: face object
		iEdge: edge array index
		iVertex: vertex array index (0 or 1)
	
	Usage:
	
		[ x, y, z ] = getVertex(gFace, 0, 1)
		
	Result:
	
		Return vertex position.
	'''
	
	vertexArr = touchTypo(iFace.Edges[iEdge])

	return [ vertexArr[iVertex].X, vertexArr[iVertex].Y, vertexArr[iVertex].Z ]


# ###################################################################################################################
def getVertexAxisCross(iA, iB):
	'''
	getVertexAxisCross(iA, iB) - get (iB - iA) value.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iA: vertex object
		iB: vertex object
	
	Usage:
	
		edgeSize = getVertexAxisCross(v0[0], v1[0])
		
	Result:
	
		Return diff for vertices values.
	'''
	
	if iA >= 0 and iB >= 0 and iB > iA:
		return iB - iA
	if iB >= 0 and iA >= 0 and iA > iB:
		return iA - iB
		
	if iA < 0 and iB >= 0 and iB > iA:
		return abs(iA) + iB
	if iB < 0 and iA >= 0 and iA > iB:
		return abs(iB) + iA

	if iA < 0 and iB <= 0 and iB > iA:
		return abs(iA) - abs(iB)
	if iB < 0 and iA <= 0 and iA > iB:
		return abs(iB) - abs(iA)

	return 0


# ###################################################################################################################
# Edges
# ###################################################################################################################


# ###################################################################################################################
def getEdgeVertices(iEdge):
	'''
	getEdgeVertices(iEdge) - get all vertices values for edge.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iEdge: edge object
		
	Usage:
	
		[ v1, v2 ] = getEdgeVertices(gEdge)
		
	Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 1, 1, 1 ] ].
	'''
	
	vertexArr = touchTypo(iEdge)

	v1 = [ vertexArr[0].X, vertexArr[0].Y, vertexArr[0].Z ]
	v2 = [ vertexArr[1].X, vertexArr[1].Y, vertexArr[1].Z ]

	return [ v1, v2 ]


# ###################################################################################################################
def getEdgeNormalized(iV1, iV2):
	'''
	getEdgeNormalized(iV1, iV2) - returns vertices with exact sorted order V1 > V2, mostly used 
	to normalize Pad vertices
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iV1: array with vertices e.g. [ 1, 1, 1 ]
		iV2: array with vertices e.g. [ 2, 2, 2 ]
	
	Usage:
	
		[ v1, v2 ] = getEdgeNormalized(v1, v2)
		
	Result:
	
		for vertices [ 2, 2, 2 ], [ 1, 1, 1 ] return [ 1, 1, 1 ], [ 2, 2, 2 ]

	'''

	# edge along X
	if iV1[0] != iV2[0]:
		if iV1[0] > iV2[0]:
			return [ iV1, iV2 ]
		else:
			return [ iV2, iV1 ]
			
	# edge along Y
	if iV1[1] != iV2[1]:
		if iV1[1] > iV2[1]:
			return [ iV1, iV2 ]
		else:
			return [ iV2, iV1 ]
			
	# edge along Z
	if iV1[2] != iV2[2]:
		if iV1[2] > iV2[2]:
			return [ iV1, iV2 ]
		else:
			return [ iV2, iV1 ]
		
	return [ iV1, iV2 ]


# ############################################################################
def getEdgeIndex(iObj, iEdge):
	'''
	getEdgeIndex(iObj, iEdge) - returns edge index for given object and edge.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object of the edge
		iEdge: edge object
	
	Usage:
	
		edgeIndex = getEdgeIndex(gObj, gEdge)
		
	Result:
	
		return int value for edge

	'''

	index = 1
	for e in iObj.Shape.Edges:
		if str(e.BoundBox) == str(iEdge.BoundBox):
			return index

		index = index + 1
	
	return -1


# ############################################################################
def getEdgeIndexByKey(iObj, iBoundBox):
	'''
	getEdgeIndexByKey(iObj, iBoundBox) - returns edge index for given edge BoundBox.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object of the edge
		iBoundBox: edge BoundBox as key
	
	Usage:
	
		edgeIndex = getEdgeIndex(o, key)
		
	Result:
	
		return int value for edge

	'''

	index = 1
	for e in iObj.Shape.Edges:
		
		c = "BoundBox ("
		c += str(int(round(e.BoundBox.XMin, 0))) + ", "
		c += str(int(round(e.BoundBox.YMin, 0))) + ", "
		c += str(int(round(e.BoundBox.ZMin, 0))) + ", "
		c += str(int(round(e.BoundBox.XMax, 0))) + ", "
		c += str(int(round(e.BoundBox.YMax, 0))) + ", "
		c += str(int(round(e.BoundBox.ZMax, 0)))
		c += ")"
		
		if c == str(iBoundBox):
			return index

		index = index + 1
	
	return -1


# ###################################################################################################################
# Faces
# ###################################################################################################################


# ############################################################################
def getFaceIndex(iObj, iFace):
	'''
	getFaceIndex(iObj, iFace) - returns face index for given object and face.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object of the face
		iFace: face object
	
	Usage:
	
		faceIndex = getFaceIndex(gObj, gFace)
		
	Result:
	
		return int value for face

	'''

	index = 1
	for f in iObj.Shape.Faces:
		if str(f.BoundBox) == str(iFace.BoundBox):
			return index

		index = index + 1
	
	return -1


# ############################################################################
def getFaceIndexByKey(iObj, iBoundBox):
	'''
	getFaceIndexByKey(iObj, iBoundBox) - returns face index for given face BoundBox.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object of the face
		iBoundBox: face BoundBox as key
	
	Usage:
	
		faceIndex = getFaceIndexByKey(o, key)
		
	Result:
	
		return int value for face

	'''

	index = 1
	for e in iObj.Shape.Faces:
		
		c = "BoundBox ("
		c += str(int(round(e.BoundBox.XMin, 0))) + ", "
		c += str(int(round(e.BoundBox.YMin, 0))) + ", "
		c += str(int(round(e.BoundBox.ZMin, 0))) + ", "
		c += str(int(round(e.BoundBox.XMax, 0))) + ", "
		c += str(int(round(e.BoundBox.YMax, 0))) + ", "
		c += str(int(round(e.BoundBox.ZMax, 0)))
		c += ")"
		
		if c == str(iBoundBox):
			return index

		index = index + 1
	
	return -1


# ###################################################################################################################
def getFaceVertices(iFace):
	'''
	getFaceVertices(iFace) - get all vertices values for face.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iFace: face object
		
	Usage:
	
		[ v1, v2, v3, v4 ] = getFaceVertices(gFace)
		
	Result:
	
		Return vertices array like [ [ 1, 1, 1 ], [ 2, 2, 2 ], [ 3, 3, 3 ], [ 4, 4, 4 ] ]
	'''
	
	vertexArr = touchTypo(iFace)

	v1 = [ vertexArr[0].X, vertexArr[0].Y, vertexArr[0].Z ]
	v2 = [ vertexArr[1].X, vertexArr[1].Y, vertexArr[1].Z ]
	v3 = [ vertexArr[2].X, vertexArr[2].Y, vertexArr[2].Z ]
	v4 = [ vertexArr[3].X, vertexArr[3].Y, vertexArr[3].Z ]
	
	return [ v1, v2, v3, v4 ]


# ###################################################################################################################
def getFaceType(iObj, iFace):
	'''
	getFaceType(iObj, iFace) - get face type, if this is "edge" or "surface".
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object where is the face
		iFace: face object

	Usage:
	
		faceType = getFaceType(gObj, gFace)
		
	Result:
	
		Return string "surface" or "edge".

	'''
	
	sizes = []
	sizes = getSizes(iObj)
	sizes.sort()
	
	t = int(sizes[0])
	
	for e in iFace.Edges:
		if int(e.Length) == t:
			return "edge"
			
	return "surface"
	

# ###################################################################################################################
def getFaceEdges(iObj, iFace):
	'''
	getFaceEdges(iObj, iFace) - get all edges for given face grouped by sizes.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object where is the face
		iFace: face object

	Usage:
	
		[ faceType, arrAll, arrThick, arrShort, arrLong ] = getFaceEdges(gObj, gFace)
		
	Result:
	
		Return arrays like [ faceType, arrAll, arrThick, arrShort, arrLong ] with edges objects, 
		
		faceType - string "surface" or "edge"
		arrAll - array with all edges
		arrThick - array with the thickness edges
		arrShort - array with the short edges (if type is edge this will be the same as arrThick)
		arrLong - array with the long edges

	'''
	
	sizes = []
	sizes = getSizes(iObj)
	sizes.sort()
	
	t = int(sizes[0])
	s = int(sizes[1])
	l = int(sizes[2])
	
	e1 = iFace.Edges[0]
	e2 = iFace.Edges[1]
	e3 = iFace.Edges[2]
	e4 = iFace.Edges[3]

	arrAll = [ e1, e2, e3, e4 ]
	arrThick = []
	arrShort = []
	arrLong = []
	
	if int(e1.Length) == t:
		arrThick.append(e1)
	if int(e1.Length) == s:
		arrShort.append(e1)
	if int(e1.Length) == l:
		arrLong.append(e1)
	
	if int(e2.Length) == t:
		arrThick.append(e2)
	if int(e2.Length) == s:
		arrShort.append(e2)
	if int(e2.Length) == l:
		arrLong.append(e2)
		
	if int(e3.Length) == t:
		arrThick.append(e3)
	if int(e3.Length) == s:
		arrShort.append(e3)
	if int(e3.Length) == l:
		arrLong.append(e3)
	
	if int(e4.Length) == t:
		arrThick.append(e4)
	if int(e4.Length) == s:
		arrShort.append(e4)
	if int(e4.Length) == l:
		arrLong.append(e4)
	
	if len(arrThick) == 0:
		faceType = "surface"
	else:
		faceType = "edge"
	
	return [ faceType, arrAll, arrThick, arrShort, arrLong ]
	

# ###################################################################################################################
def getFacePlane(iFace):
	'''
	getFacePlane(iFace) - get face plane in notation "XY", "XZ", "YZ". 

	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iFace: face object
	
	Usage:
	
		plane = getFacePlane(face)
		
	Result:
	
		string "XY", "XZ", or "YZ".
		
	'''

	[ v1, v2, v3, v4 ] = getFaceVertices(iFace)

	if int(v1[2] + v2[2] + v3[2] + v4[2]) == int(4 * v1[2]):
		return "XY"
	
	if int(v1[1] + v2[1] + v3[1] + v4[1]) == int(4 * v1[1]):
		return "XZ"
	
	if int(v1[0] + v2[0] + v3[0] + v4[0]) == int(4 * v1[0]):
		return "YZ"

	return ""


# ###################################################################################################################
def getFaceSink(iObj, iFace):
	'''
	getFaceSink(iObj, iFace) - get face sink axis direction in notation "+", or "-".

	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object with the face
		iFace: face object
	
	Usage:
	
		sink = getFaceSink(obj, face)
		
	Result:
	
		string "+" if the object at face should go along axis forward, 
		or "-" if the object at face should go along axis backward
		
	'''

	plane = getFacePlane(iFace)
	[ x, y, z ] = iFace.CenterOfMass
	
	if plane == "XY":
		v = FreeCAD.Vector(x, y, z + 1)
		
	if plane == "XZ":
		v = FreeCAD.Vector(x, y + 1, z)
		
	if plane == "YZ":
		v = FreeCAD.Vector(x + 1, y, z)
		
	inside = iObj.Shape.BoundBox.isInside(v)
	
	if inside == True:
		return "+"
	else:
		return "-"


# ###################################################################################################################
def getFaceObjectRotation(iObj, iFace):
	'''
	getFaceObjectRotation(iObj, iFace) - get face object rotation to apply to the new created object at face. 
	Object created at face with this rotation should be up from the face.

	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object with the face
		iFace: face object
	
	Usage:
	
		r = getFaceObjectRotation(obj, face)
		
	Result:
	
		FreeCAD.Rotation object that can be directly pass to the setPlacement or object.Placement
		
	'''

	plane = getFacePlane(iFace)
	sink = getFaceSink(iObj, iFace)
	
	if sink == "+":
				
		if plane == "XY":
			r = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 180)
			
		if plane == "XZ":
			r = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 90)

		if plane == "YZ":
			r = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), 270)

	else:
	
		if plane == "XY":
			r = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 0)
			
		if plane == "XZ":
			r = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 270)

		if plane == "YZ":
			r = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), 90)
	
	return r


# ###################################################################################################################
def getFaceDetails(iObj, iFace):
	'''
	getFaceDetails(iObj, iFace) - allow to get detailed information for face direction.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: selected object
		iFace: selected face object
	
	Usage:
	
		getFaceDetails(gObj, gFace)
		
	Result:
	
		[ "XY", "surface" ] - if the direction is XY and it is surface, no thickness edge
		[ "XY", "edge" ] - if the direction is XY and it is edge, there is thickness edge
		[ "XY", "equal" ] - if the direction is XY and both edges are equal
		
		Note: The first argument can be "XY", "YX", "XZ", "ZX", "YZ", "ZY". 
		This is related to face not to object. The object direction will be different.
		
	'''

	[ v1, v2, v3, v4 ] = getFaceVertices(iFace)

	direction = ""
	
	if int(v1[2] + v2[2] + v3[2] + v4[2]) == int(4 * v1[2]):
		direction = "XY"
	
	if int(v1[1] + v2[1] + v3[1] + v4[1]) == int(4 * v1[1]):
		direction = "XZ"
	
	if int(v1[0] + v2[0] + v3[0] + v4[0]) == int(4 * v1[0]):
		direction = "YZ"

	s = getSizes(iObj)
	s.sort()
	thick = int(s[0])
	
	e1 = int(iFace.Edges[0].Length)
	e2 = int(iFace.Edges[1].Length)
	e3 = int(iFace.Edges[2].Length)
	e4 = int(iFace.Edges[3].Length)
	
	ed = int(iFace.Edges[0].Length + iFace.Edges[1].Length + iFace.Edges[2].Length + iFace.Edges[3].Length)
	
	if ed == int(4 * e1):
		return [ direction, "equal" ]
	
	if iObj.isDerivedFrom("Part::Box"):
		
		if direction == "XY" and e1 < e2:
			if e1 == thick or e2 == thick:
				return [ "XY", "edge" ]
			else:
				return [ "XY", "surface" ]

		if direction == "XY" and e1 > e2:
			if e1 == thick or e2 == thick:
				return [ "YX", "edge" ]
			else:
				return [ "YX", "surface" ]

		if direction == "XZ" and e1 > e2:
			if e1 == thick or e2 == thick:
				return [ "XZ", "edge" ]
			else:
				return [ "XZ", "surface" ]

		if direction == "XZ" and e1 < e2:
			if e1 == thick or e2 == thick:
				return [ "ZX", "edge" ]
			else:
				return [ "ZX", "surface" ]

		if direction == "YZ" and e1 < e2:
			if e1 == thick or e2 == thick:
				return [ "YZ", "edge" ]
			else:
				return [ "YZ", "surface" ]

		if direction == "YZ" and e1 > e2:
			if e1 == thick or e2 == thick:
				return [ "ZY", "edge" ]
			else:
				return [ "ZY", "surface" ]

	else:
		
		return [ "not supported", "not supported" ]


# ###################################################################################################################
# Object
# ###################################################################################################################


# ###################################################################################################################
def getReference(iObj="none"):
	'''
	getReference(iObj="none") - get reference to the selected or given object.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj (optional): object to get reference (to return base object)
	
	Usage:
	
		gObj = getReference()
		
	Result:
	
		obj - reference to the base object

	'''

	if iObj == "none":
		obj = FreeCADGui.Selection.getSelection()[0]
	else:
		obj = iObj

	if ( 
		obj.isDerivedFrom("PartDesign::Thickness") or 
		obj.isDerivedFrom("PartDesign::Chamfer")
		):
		return obj.Base[0]
	else:
		return obj
	
	return -1


# ###################################################################################################################
def getPlacement(iObj):
	'''
	getPlacement(iObj) - get placement with rotation info for given object.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object to get placement

	Usage:
	
		[ x, y, z, r ] = getPlacement(gObj)
		
	Result:
	
		return [ x, y, z, r ] array with placement info, where:
		
		x: X Axis object position
		y: Y Axis object position
		z: Z Axis object position
		r: Rotation object

	'''

	if iObj.isDerivedFrom("PartDesign::Pad"):
		ref = iObj.Profile[0].AttachmentOffset
		
	elif iObj.isDerivedFrom("Sketcher::SketchObject"):
		ref = iObj.AttachmentOffset
	else:
		ref = iObj.Placement
		
	x = ref.Base.x
	y = ref.Base.y
	z = ref.Base.z
	r = ref.Rotation

	return [ x, y, z, r ]


# ###################################################################################################################
def setPlacement(iObj, iX, iY, iZ, iR):
	'''
	setPlacement(iObj, iX, iY, iZ, iR) - set placement with rotation for given object.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object to set custom placement and rotation
		iX: X Axis object position
		iX: Y Axis object position
		iZ: Z Axis object position
		iR: Rotation object

	Usage:
	
		setPlacement(gObj, 100, 100, 200, r)
		
	Result:
	
		Object gObj should be moved into 100, 100, 200 position without rotation.

	'''

	if iObj.isDerivedFrom("PartDesign::Pad"):
		iObj.Profile[0].AttachmentOffset.Base = FreeCAD.Vector(iX, iY, iZ)
		iObj.Profile[0].AttachmentOffset.Rotation = iR
		
	elif iObj.isDerivedFrom("Sketcher::SketchObject"):
		iObj.Placement.Base = FreeCAD.Vector(iX, iY, iZ)
		iObj.Placement.Rotation = iR
		
	else:
		iObj.Placement.Base = FreeCAD.Vector(iX, iY, iZ)
		iObj.Placement.Rotation = iR
	

# ###################################################################################################################
def resetPlacement(iObj):
	'''
	resetPlacement(iObj) - reset placement for given object. Needed to set rotation for object at face.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object to reset placement

	Usage:
	
		resetPlacement(obj)
		
	Result:
	
		Object obj return to base position.

	'''

	zero = FreeCAD.Vector(0, 0, 0)
	r = FreeCAD.Rotation(FreeCAD.Vector(0.00, 0.00, 1.00), 0.00)
	
	if iObj.isDerivedFrom("PartDesign::Pad"):
		iObj.Profile[0].AttachmentOffset.Base = zero
		iObj.Profile[0].AttachmentOffset.Rotation = r
		
	elif iObj.isDerivedFrom("Sketcher::SketchObject"):
		iObj.Placement.Base = zero
		iObj.Placement.Rotation = r
		
	else:
		iObj.Placement.Base = zero
		iObj.Placement.Rotation = r


# ###################################################################################################################
def getModelRotation(iX, iY, iZ):
	'''
	getModelRotation() - transform given iX, iY, iZ values to the correct vector, if the user rotated 3D model.

	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iX: X value to transform
		iY: Y value to transform
		iY: Z value to transform
	
	Usage:
	
		[x, y, z ] = getModelRotation(x, y, z)
		
	Result:
	
		[ X, Y, Z ] - transformed vector of given values

	'''

	[ x, y, z ] = FreeCADGui.ActiveDocument.ActiveView.getViewDirection()
	[ px, py, pz ] = FreeCADGui.ActiveDocument.ActiveView.viewPosition().Rotation.getYawPitchRoll()
	
	# init 0 key
	X = iX
	Y = iY
	Z = iZ

	# X axis invert
	if x > 0:
		X = -iX
	
	# Y axis invert
	if y < 0:
		Y = -iY
		
	# Z axis invert
	if z > 0:
		Z = -iZ

	# did I say rotation? ;-) they see me rolling ;-)

	# ##################################################
	# Z up, X rotation
	# ##################################################

	# Z up, X rotate 0
	# is base state

	# Z up, X rotate 1
	if x < 0 and y < 0 and z < 0 and py < 0 and pz > 0:
		X = -iY
		Y = iX
		Z = iZ
		
	# Z up, X rotate 2
	if x > 0 and y < 0 and z < 0 and py < 0 and pz > 0:
		X = -iX
		Y = -iY
		Z = iZ

	# Z up, X rotate 3
	if x > 0 and y > 0 and z < 0 and py < 0 and pz > 0:
		X = iY
		Y = -iX
		Z = iZ

	# ##################################################
	# Z down, X rotation
	# ##################################################

	# Z down, X rotate 0
	if x < 0 and y < 0 and z > 0 and py > 0 and pz < 0:
		X = iX
		Y = -iY
		Z = -iZ

	# Z down, X rotate 1
	if x < 0 and y > 0 and z > 0 and py > 0 and pz < 0:
		X = -iY
		Y = -iX
		Z = -iZ

	# Z down, X rotate 2
	if x > 0 and y > 0 and z > 0 and py > 0 and pz < 0:
		X = -iX
		Y = iY
		Z = -iZ

	# Z down, X rotate 3
	if x > 0 and y < 0 and z > 0 and py > 0 and pz < 0:
		X = iY
		Y = iX
		Z = -iZ

	# ##################################################
	# X up, Y rotation
	# ##################################################

	# X up, Y rotate 0
	if x < 0 and y > 0 and z > 0 and py > 0 and pz > 0:
		X = iZ
		Y = iY
		Z = -iX
	
	# X up, Y rotate 1
	if x < 0 and y < 0 and z > 0 and py < 0 and pz > 0:
		X = iZ
		Y = iX
		Z = iY
		
	# X up, Y rotate 2
	if x < 0 and y < 0 and z < 0 and py < 0 and pz < 0:
		X = iZ
		Y = -iY
		Z = iX

	# X up, Y rotate 3
	if x < 0 and y > 0 and z < 0 and py > 0 and pz < 0:
		X = iZ
		Y = -iX
		Z = -iY

	# ##################################################
	# X down, Y rotation
	# ##################################################

	# X down, Y rotate 0
	if x > 0 and y > 0 and z < 0 and py < 0 and pz < 0:
		X = -iZ
		Y = iY
		Z = iX
	
	# X down, Y rotate 1
	if x > 0 and y < 0 and z < 0 and py > 0 and pz < 0:
		X = -iZ
		Y = iX
		Z = -iY
	
	# X down, Y rotate 2
	if x > 0 and y < 0 and z > 0 and py > 0 and pz > 0:
		X = -iZ
		Y = -iY
		Z = -iX
	
	# X down, Y rotate 3
	if x > 0 and y > 0 and z > 0 and py < 0 and pz > 0:
		X = -iZ
		Y = -iX
		Z = iY

	# ##################################################
	# Y up, X rotation
	# ##################################################

	# Y up, X rotate 0
	if x < 0 and y < 0 and z < 0 and py > 0 and pz < 0:
		X = iX
		Y = iZ
		Z = -iY
	
	# Y up, X rotate 1
	if x < 0 and y < 0 and z > 0 and py > 0 and pz > 0:
		X = -iY
		Y = iZ
		Z = -iX

	# Y up, X rotate 2
	if x > 0 and y < 0 and z > 0 and py < 0 and pz > 0:
		X = -iX
		Y = iZ
		Z = iY
	
	# Y up, X rotate 3
	if x > 0 and y < 0 and z < 0 and py < 0 and pz < 0:
		X = iY
		Y = iZ
		Z = iX
	
	# ##################################################
	# Y down, X rotation
	# ##################################################

	# Y down, X rotate 0
	if x < 0 and y > 0 and z > 0 and py < 0 and pz > 0:
		X = iX
		Y = -iZ
		Z = iY

	# Y down, X rotate 1
	if x < 0 and y > 0 and z < 0 and py < 0 and pz < 0:
		X = -iY
		Y = -iZ
		Z = iX
	
	# Y down, X rotate 2
	if x > 0 and y > 0 and z < 0 and py > 0 and pz < 0:
		X = -iX
		Y = -iZ
		Z = -iY
	
	# Y down, X rotate 3
	if x > 0 and y > 0 and z > 0 and py > 0 and pz > 0:
		X = iY
		Y = -iZ
		Z = -iX
	
	return [ X, Y, Z ]


# ###################################################################################################################
def getSizes(iObj):
	'''
	getSizes(iObj) - allow to get sizes for object (iObj), according to the object type. The values are not sorted.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object to get sizes
	
	Usage:
	
		[ size1, size2, size3 ] = getSizes(obj)
		
	Result:
	
		Returns [ Length, Width, Height ] for Cube.
	'''

	if iObj.isDerivedFrom("Part::Box"):

		return [ iObj.Length.Value, iObj.Width.Value, iObj.Height.Value ]
			
	if iObj.isDerivedFrom("PartDesign::Pad"):

		for c in iObj.Profile[0].Constraints:
			if c.Name == "SizeX":
				sizeX = c.Value
			if c.Name == "SizeY":
				sizeY = c.Value
				
		return [ sizeX, sizeY, iObj.Length.Value ]

	try:
		
		return [ iObj.Base_Width.Value, iObj.Base_Height.Value, iObj.Base_Length.Value ]
		
	except:
		
		# allows to move all furniture more quickly
		return [ 100, 100, 100 ]


# ###################################################################################################################
def getDirection(iObj):
	'''
	getDirection(iObj) - allow to get Cube object direction (iType).
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: selected object
	
	Usage:
	
		getDirection(obj)
		
	Result:
	
		Returns iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"
	'''

	if iObj.isDerivedFrom("Part::Box"):
		
		if (
			iObj.Height.Value < iObj.Width.Value and iObj.Height.Value < iObj.Length.Value and 
			iObj.Width.Value <= iObj.Length.Value
			):
			return "XY"
		
		if (
			iObj.Height.Value < iObj.Width.Value and iObj.Height.Value < iObj.Length.Value and 
			iObj.Width.Value > iObj.Length.Value
			):
			return "YX"
		
		if (
			iObj.Width.Value < iObj.Height.Value and iObj.Width.Value < iObj.Length.Value and 
			iObj.Height.Value <= iObj.Length.Value
			):
			return "XZ"
			
		if (
			iObj.Width.Value < iObj.Height.Value and iObj.Width.Value < iObj.Length.Value and 
			iObj.Height.Value > iObj.Length.Value
			):
			return "ZX"
			
		if (
			iObj.Length.Value < iObj.Height.Value and iObj.Length.Value < iObj.Width.Value and 
			iObj.Height.Value <= iObj.Width.Value
			):
			return "YZ"
			
		if (
			iObj.Length.Value < iObj.Height.Value and iObj.Length.Value < iObj.Width.Value and 
			iObj.Height.Value > iObj.Width.Value
			):
			return "ZY"

		# for profiles with 2 equal sizes
		
		if iObj.Height.Value == iObj.Width.Value and iObj.Length.Value >= iObj.Height.Value:
			return "XY"
			
		if iObj.Length.Value == iObj.Height.Value and iObj.Width.Value > iObj.Height.Value:
			return "YX"
			
		if iObj.Length.Value == iObj.Width.Value and iObj.Height.Value > iObj.Width.Value:
			return "ZX"

	else:
		
		ref = iObj.Profile[0].Support[0][0]
		[ sX, sY, thick ] = getSizes(iObj)
		
		if ref.Label.startswith("XY"):
			
			if sX >= sY:
				return "XY"
			
			if sX < sY:
				return "YX"
			
		if ref.Label.startswith("XZ"):
			
			if sX >= sY:
				return "XZ"
			
			if sX < sY:
				return "ZX"
			
		if ref.Label.startswith("YZ"):
			
			if sX >= sY:
				return "YZ"
			
			if sX < sY:
				return "ZY"


# ###################################################################################################################
def convertPosition(iObj, iX, iY, iZ):
	'''
	convertPosition(iObj, iX, iY, iZ) - convert given position vector to correct position values according 
	to the object direction.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object
		iX: x position
		iY: y position
		iZ: z position
	
	Usage:
	
		convertPosition(obj, 0, 400, 0)
		
	Result:
	
		For Pad object in XZ direction return the AttachmentOffset order [ 0, 0, -400 ]
	'''
	
	if iObj.isDerivedFrom("PartDesign::Pad"):
		
		direction = getDirection(iObj)
		
		if direction == "XY" or direction == "YX":
			return [ iX, iY, iZ ]
		
		if direction == "XZ" or direction == "ZX":
			return [ iX, iZ, -iY ]

		if direction == "YZ" or direction == "ZY":
			return [ iY, iZ, iX ]
	
	else:
		
		return [ iX, iY, iZ ]


# ###################################################################################################################
def sizesToCubePanel(iObj, iType):
	'''
	sizesToCubePanel(iObj, iType) - converts selected object (iObj) sizes to Cube panel sizes into given direction (iType). 
	So, the returned values can be directly assigned to Cube object in order to create 
	panel in exact direction.

	Note: This is internal function, so there is no error pop-up or any error handling.

	Args:

		iObj: selected object
		iType direction: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

	Usage:

		[ Length, Width, Height ] = sizesToCubePanel(obj, "YZ")
		
	Result:

		Returns [ Length, Width, Height ] for YZ object placement".
	'''

	if iObj.isDerivedFrom("Part::Box"):

		sizes = [ iObj.Length.Value, iObj.Width.Value, iObj.Height.Value ]
		
	elif iObj.isDerivedFrom("PartDesign::Pad"):
		
		for c in iObj.Profile[0].Constraints:
			if c.Name == "SizeX":
				sizeX = c.Value
			if c.Name == "SizeY":
				sizeY = c.Value
		
		sizes = [ iObj.Length.Value, sizeX, sizeY ]
	
	else:
		
		sizes = [ iObj.Base_Length.Value, iObj.Base_Width.Value, iObj.Base_Height.Value ]

	sizes.sort()

	if iType == "XY":
		Length = sizes[2]
		Width = sizes[1]
		Height = sizes[0]

	if iType == "YX":
		Length = sizes[1]
		Width = sizes[2]
		Height = sizes[0]

	if iType == "XZ":
		Length = sizes[2]
		Width = sizes[0]
		Height = sizes[1]

	if iType == "ZX":
		Length = sizes[1]
		Width = sizes[0]
		Height = sizes[2]

	if iType == "YZ":
		Length = sizes[0]
		Width = sizes[2]
		Height = sizes[1]

	if iType == "ZY":
		Length = sizes[0]
		Width = sizes[1]
		Height = sizes[2]

	return [ Length, Width, Height ]


# ###################################################################################################################
def makeCuts(iObjects):
	'''
	makeCuts(iObjects) - allows to create multi bool cut operation at given objects. First objects 
	from iObjects is the base element and all other will cut the base. The copies will be created for cut. 
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObjects: objects to parse by multi bool cut

	Usage:
	
		import MagicPanels
		MagicPanels.makeCuts(objects)
		
	Result:
	
		Array of cut objects will be returned.
	'''
	
	cuts = []
	
	i = 0
	for o in iObjects:
		
		i = i + 1
		
		if i == 1:
			base = o
			baseName = str(base.Name)
			baseLabel = str(base.Label)
			continue

		copy = FreeCAD.ActiveDocument.copyObject(o)
		copy.Label = "copy, " + o.Label
		
		cutName = baseName + str(i-1)
		cut = FreeCAD.ActiveDocument.addObject("Part::Cut", cutName)
		cut.Base = base
		cut.Tool = copy
		cut.Label = "Cut " + str(i-1) + ", " + baseLabel
		
		FreeCAD.activeDocument().recompute()
		
		base = cut
		cuts.append(cut)
		
	cut.Label = "Cut, " + baseLabel

	return cuts


# ###################################################################################################################
def makePad(iObj, iPadLabel="Pad"):
	'''
	makePad(iObj, iPadLabel="Pad") - allows to create Part, Plane, Body, Pad, Sketch objects.
	
	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iObj: object Cube to change into Pad
		iPadLabel: Label for the new created Pad, the Name will be Pad
		
	Usage:
	
		import MagicPanels
		MagicPanels.makePad(obj, "myPanel")
		
	Result:
	
		Created Pad with correct placement, rotation and return [ part, body, sketch, pad ].
	'''

	sizes = getSizes(iObj)
	sizes.sort()
	
	direction = getDirection(iObj)
	
	if direction == "XY" or direction == "XZ" or direction == "YZ":
		s = [ sizes[2], sizes[1], sizes[0] ]
	
	if direction == "YX" or direction == "ZX" or direction == "ZY":
		s = [ sizes[1], sizes[2], sizes[0] ]

	[ X, Y, Z, r ] = getPlacement(iObj)
	
	if direction == "XY" or direction == "YX":
		[ x, y, z ] = [ X, Y, Z ]
	
	if direction == "XZ" or direction == "ZX":
		[ x, y, z ] = [ X, Z, -(Y+sizes[0]) ]

	if direction == "YZ" or direction == "ZY":
		[ x, y, z ] = [ Y, Z, X ]
	
	import Part, PartDesign
	import Sketcher
	import PartDesignGui

	doc = FreeCAD.ActiveDocument
	
	part = doc.addObject('App::Part', 'Part')
	part.Label = "Part, "+iPadLabel
	
	body = doc.addObject('PartDesign::Body', 'Body')
	body.Label = "Body, "+iPadLabel
	part.addObject(body)
	
	sketch = body.newObject('Sketcher::SketchObject', 'Sketch')
	sketch.Label = "Pattern, "+iPadLabel
	
	if direction == "XY" or direction == "YX":
		sketch.Support = (body.Origin.OriginFeatures[3])
	if direction == "XZ" or direction == "ZX":
		sketch.Support = (body.Origin.OriginFeatures[4])
	if direction == "YZ" or direction == "ZY":
		sketch.Support = (body.Origin.OriginFeatures[5])

	sketch.MapMode = 'FlatFace'

	geoList = []
	geoList.append(Part.LineSegment(FreeCAD.Vector(115.695488,159.435455,0),FreeCAD.Vector(274.784485,159.435455,0)))
	geoList.append(Part.LineSegment(FreeCAD.Vector(274.784485,159.435455,0),FreeCAD.Vector(274.784485,53.166523,0)))
	geoList.append(Part.LineSegment(FreeCAD.Vector(274.784485,53.166523,0),FreeCAD.Vector(115.695488,53.166523,0)))
	geoList.append(Part.LineSegment(FreeCAD.Vector(115.695488,53.166523,0),FreeCAD.Vector(115.695488,159.435455,0)))
	sketch.addGeometry(geoList,False)
	
	conList = []
	conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
	conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
	conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
	conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
	conList.append(Sketcher.Constraint('Horizontal',0))
	conList.append(Sketcher.Constraint('Horizontal',2))
	conList.append(Sketcher.Constraint('Vertical',1))
	conList.append(Sketcher.Constraint('Vertical',3))
	sketch.addConstraint(conList)
	del geoList, conList

	sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,-1,1))
	sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,274.784485))
	sketch.setDatum(9,FreeCAD.Units.Quantity(s[0]))
	sketch.renameConstraint(9, u'SizeX')
	sketch.addConstraint(Sketcher.Constraint('DistanceY',3,1,3,2,159.435455))
	sketch.setDatum(10,FreeCAD.Units.Quantity(s[1]))
	sketch.renameConstraint(10, u'SizeY')

	position = FreeCAD.Vector(x, y, z)
	sketch.AttachmentOffset = FreeCAD.Placement(position, r)

	pad = body.newObject('PartDesign::Pad', "Pad")
	pad.Label = iPadLabel
	pad.Profile = sketch
	pad.Length = FreeCAD.Units.Quantity(s[2])
	sketch.Visibility = False

	doc.recompute()

	return [ part, body, sketch, pad ]


# ###################################################################################################################
def makeHoles(iObj, iFace, iCylinders):
	'''
	makeHoles(iObj, iFace, iCylinders) - make holes

	Note: This is internal function, so there is no error pop-up or any error handling.

	Args:

		iObj: base object to make hole
		iFace: face of base object to make hole
		iCylinders: list of cylinders to make holes below each one

	Usage:

		import MagicPanels
		holes = MagicPanels.makeHoles(obj, face, cylinders)
		
	Result:

		Make holes and return list of holes.
	'''

	import Part, Sketcher

	holes = []

	base = iObj
	face = iFace
	objects = iCylinders

	# set body for base object
	if base.isDerivedFrom("Part::Box"):
		
		[ part, body, sketch, pad ] = makePad(base, base.Label)
		FreeCAD.ActiveDocument.removeObject(base.Name)
		FreeCAD.activeDocument().recompute()
	
	else:
		
		body = base._Body

	# loop in drill bits and drill holes
	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = o.Placement.Rotation.Axis
		circleGeo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, o.Radius)
		holeSketch.addGeometry(circleGeo, False)
		
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1)) 
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 0, 2 * o.Radius)) 
		s = str(float(2 * o.Radius))+" mm"
		holeSketch.setDatum(1, FreeCAD.Units.Quantity(s))
		holeSketch.renameConstraint(1, u'Hole00Diameter')
		
		FreeCAD.ActiveDocument.recompute()
		
		# set position to hole Sketch
		[ x, y, z, r ] = getPlacement(o)
		setPlacement(holeSketch, x, y, z, r)
		
		FreeCAD.ActiveDocument.recompute()
		
		# create hole object
		hole = body.newObject('PartDesign::Hole','Hole')
		hole.Profile = holeSketch
		holeSketch.Visibility = False
		
		hole.Diameter = 2 * o.Radius
		hole.HoleCutDiameter = 2 * o.Radius
		hole.HoleCutDepth = o.Height
		hole.HoleCutCountersinkAngle = 90.000000
		hole.Depth = o.Height
		hole.DrillPointAngle = 118.000000
		hole.TaperedAngle = 90.000000
		hole.Threaded = 0
		hole.ThreadType = 0
		hole.HoleCutType = 0
		hole.DepthType = 0
		hole.DrillPoint = 1
		hole.DrillForDepth = 1
		hole.Tapered = 0
		
		FreeCAD.ActiveDocument.recompute()
		
		base = hole
		holes.append(hole)

	return holes
	

# ###################################################################################################################
def makeCountersinks(iObj, iFace, iCones):
	'''
	makeCountersinks(iObj, iFace, iCones) - make countersinks

	Note: This is internal function, so there is no error pop-up or any error handling.

	Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

	Usage:

		import MagicPanels
		holes = MagicPanels.makeCountersinks(obj, face, cones)
		
	Result:

		Make holes and return list of holes. 
	'''

	import Part, Sketcher

	holes = []

	base = iObj
	face = iFace
	objects = iCones
		
	# set body for base object
	if base.isDerivedFrom("Part::Box"):
		
		[ part, body, sketch, pad ] = makePad(base, base.Label)
		FreeCAD.ActiveDocument.removeObject(base.Name)
		FreeCAD.activeDocument().recompute()
	
	else:
		
		body = base._Body
	
	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = o.Placement.Rotation.Axis
		r1 = float(2 * o.Radius1)
		r2 = float(2 * o.Radius2)
		sr1 = str(r1)+" mm"
		sr2 = str(r2)+" mm"
		
		# set hole
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r1)
		holeSketch.addGeometry(geo, False)
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 0, r1)) 
		holeSketch.setDatum(1, FreeCAD.Units.Quantity(sr1))
		holeSketch.renameConstraint(1, u'Hole00Diameter')
		
		# set countersink
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r2)
		holeSketch.addGeometry(geo, True)
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 1, 3, -1, 1)) 
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 1, r2)) 
		holeSketch.setDatum(3, FreeCAD.Units.Quantity(sr2))
		holeSketch.renameConstraint(3, u'Countersink00Diameter')
		
		FreeCAD.ActiveDocument.recompute()
		
		# set position to hole Sketch
		[ x, y, z, r ] = getPlacement(o)
		setPlacement(holeSketch, x, y, z, r)
		
		FreeCAD.ActiveDocument.recompute()
		
		# create hole object
		hole = body.newObject('PartDesign::Hole','Countersink')
		hole.Profile = holeSketch
		holeSketch.Visibility = False
		
		hole.Diameter = 2 * o.Radius1
		hole.HoleCutDiameter = 2 * o.Radius2
		hole.HoleCutDepth = 5.000000
		hole.HoleCutCountersinkAngle = 90.000000
		hole.Depth = o.Height
		hole.DrillPointAngle = 118.000000
		hole.TaperedAngle = 90.000000
		hole.Threaded = 0
		hole.ThreadType = 0
		hole.HoleCutType = 2
		hole.DepthType = 0
		hole.DrillPoint = 1
		hole.DrillForDepth = 1
		hole.Tapered = 0
		
		FreeCAD.ActiveDocument.recompute()
		
		base = hole
		holes.append(hole)
		
	return holes
	

# ###################################################################################################################
def makeCounterbores(iObj, iFace, iCones):
	'''
	makeCounterbores(iObj, iFace, iCones) - make counterbores

	Note: This is internal function, so there is no error pop-up or any error handling.

	Args:

		iObj: base object to drill
		iFace: face of base object to drill
		iCones: list of drill bits to drill below each one (Cone objects)

	Usage:

		import MagicPanels
		holes = MagicPanels.drillCounterbores(obj, face, cones)
		
	Result:

		Make holes and return list of holes. 
	'''

	import Part, Sketcher

	holes = []

	base = iObj
	face = iFace
	objects = iCones
		
	# set body for base object
	if base.isDerivedFrom("Part::Box"):
		
		[ part, body, sketch, pad ] = makePad(base, base.Label)
		FreeCAD.ActiveDocument.removeObject(base.Name)
		FreeCAD.activeDocument().recompute()
	
	else:
		
		body = base._Body

	for o in objects:
		
		# create hole Sketch
		holeSketch = body.newObject('Sketcher::SketchObject','Sketch')
		holeSketch.MapMode = 'FlatFace'

		axis = o.Placement.Rotation.Axis
		r1 = float(2 * o.Radius1)
		r2 = float(2 * o.Radius2)
		sr1 = str(r1)+" mm"
		sr2 = str(r2)+" mm"
		
		# set hole
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r1)
		holeSketch.addGeometry(geo, False)
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 0, r1)) 
		holeSketch.setDatum(1, FreeCAD.Units.Quantity(sr1))
		holeSketch.renameConstraint(1, u'Hole00Diameter')
		
		# set counterbore
		geo = Part.Circle(FreeCAD.Vector(0, 0, 0), axis, r2)
		holeSketch.addGeometry(geo, True)
		holeSketch.addConstraint(Sketcher.Constraint('Coincident', 1, 3, -1, 1)) 
		holeSketch.addConstraint(Sketcher.Constraint('Diameter', 1, r2)) 
		holeSketch.setDatum(3, FreeCAD.Units.Quantity(sr2))
		holeSketch.renameConstraint(3, u'Counterbore00Diameter')
		
		FreeCAD.ActiveDocument.recompute()
		
		# set position to hole Sketch
		[ x, y, z, r ] = getPlacement(o)
		setPlacement(holeSketch, x, y, z, r)
		
		FreeCAD.ActiveDocument.recompute()
		
		# create hole object
		hole = body.newObject('PartDesign::Hole','Counterbore')
		hole.Profile = holeSketch
		holeSketch.Visibility = False
		
		hole.Diameter = r1
		hole.HoleCutDiameter = r2
		hole.HoleCutDepth = 5.000000
		hole.HoleCutCountersinkAngle = 90.000000
		hole.Depth = o.Height
		hole.TaperedAngle = 90.000000
		hole.Threaded = 0
		hole.ThreadType = 0
		hole.HoleCutType = 1
		hole.DepthType = 0
		hole.DrillPoint = 0
		hole.Tapered = 0
		
		FreeCAD.ActiveDocument.recompute()
		
		base = hole
		holes.append(hole)
		
	return holes


# ###################################################################################################################
def showInfo(iCaller, iInfo, iNote="yes"):
	'''
	showInfo(iCaller, iInfo, iNote="yes") - allow to show Gui info box for all available function and multiple calls.

	Note: This is internal function, so there is no error pop-up or any error handling.
	
	Args:
	
		iCaller: window title
		iInfo: HTML text to show
		iNote: additional tutorial ("yes" or "no"), by default is "yes".
	
	Usage:
	
		showInfo("panel"+iType, info)
		
	Result:
	
		Show info Gui.
	'''

	info = ""
	
	import os, sys
	import fakemodule
	path = os.path.dirname(fakemodule.__file__)
	iconPath = str(os.path.join(path, "Icons"))
	
	filename = ""
	
	info += '<table cellpadding="5" border="0" text-align="left">'
	info += '<tr>'
	
	info += '<td>'
	info += iInfo
	info += '</td>'
	
	info += '<td>'
	
	f = os.path.join(iconPath, iCaller+".xpm")
	if os.path.exists(f):
		filename = f
		info += '<img src="'+ filename + '" width="200" height="200" align="right"/>'
	
	f = os.path.join(iconPath, iCaller+".svg")
	if os.path.exists(f):
		filename = f
		info += '<svg>'
		info += '<img src="'+ filename + '" width="200" height="200" align="right"/>'
		info += '</svg>'
		
	f = os.path.join(iconPath, iCaller+".png")
	if os.path.exists(f):
		filename = f
		info += '<img src="'+ filename + '" width="200" height="200" align="right">'
	
	info += '</td>'
	
	info += '</tr>'
	info += '</table>'


	if iNote == "yes":
		
		info += translate('showInfoAll', 'To keep furniture designing process quick and simple, ')
		info += translate('showInfoAll', 'the furniture designing process should follow steps: ')
		
		info += '<ol>'
		
		info += '<li>'
		info += translate('showInfoAll', 'Create furniture with simple Cube panels. Try to not make detailed model ')
		info += translate('showInfoAll', 'with Pads and Sketches at this stage. ')
		info += '</li>'
		
		info += '<li>'
		info += translate('showInfoAll', 'Add simple mounting points with magicDowels tool and other simple references ')
		info += translate('showInfoAll', 'with Cubes to replace all of them later with single click.')
		info += '</li>'
		
		info += '<li>'
		info += translate('showInfoAll', 'Replace desired Cube elements with more detailed elements. Use dedicated replace ')
		info += translate('showInfoAll', 'features for that e.g. panel2profile to replace all Cubes with detailed construction ')
		info += translate('showInfoAll', 'profiles or use panel2link to replace all selected Cubes with any detailed object.')
		info += '</li>'
		
		info += '<li>'
		info += translate('showInfoAll', 'Add decorations or more details, if needed. If you want to change Cube shape you can ')
		info += translate('showInfoAll', 'replace it with Pad by single click via panel2pad replace feature and edit the Sketch. ')
		info += '</li>'
		
		info += '<li>'
		info += translate('showInfoAll', 'Add colors or textures and preview furniture.')
		info += '</li>'
		
		info += '<li>'
		info += translate('showInfoAll', 'Generate cut-list with getDimensions tool. You can use TechDraw for more detailed draw. ')
		info += '</li>'
		
		info += '<li>'
		info += translate('showInfoAll', 'You can print this report directly from TechDraw page or use sheet2export tool.')
		info += '</li>'
		
		info += '<li>'
		info += translate('showInfoAll', 'Create furniture in real-life.')
		info += '</li>'
		
		info += '<li>'
		info += translate('showInfoAll', 'Have fun with your new furniture in real-life !')
		info += '</li>'
		
		info += '</ol>'
			
		info += translate('showInfoAll', 'For more details please see:')
		info += ' ' + '<a href="https://github.com/dprojects/Woodworking">'
		info += translate('showInfoAll', 'Woodworking workbench documentation.')
		info += '</a>'
	
	msg = QtGui.QMessageBox()
	msg.setWindowTitle(iCaller)
	msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
	msg.setText(info)
	msg.exec_()


# ###################################################################################################################
# Functions - for external usage, should be error handling and pop-up.
# ###################################################################################################################


# ###################################################################################################################
def panelDefault(iType):
	'''
	panelDefault(iType) - allows to create default panel 600 x 300 x 18 into exact direction (iType).

	Note: This function displays pop-up info in case of error.

	Args:

		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

	Usage:

		import MagicPanels
		
		MagicPanels.panelDefault("XY")
		
	Result:

		Created panel 600 x 300 x 18 with correct direction XY.
	'''

	try:

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panel"+iType)

		if iType == "XY":
			panel.Length = 600
			panel.Width = 300
			panel.Height = 18

		if iType == "YX":
			panel.Length = 300
			panel.Width = 600
			panel.Height = 18

		if iType == "XZ":
			panel.Length = 600
			panel.Width = 18
			panel.Height = 300

		if iType == "ZX":
			panel.Length = 300
			panel.Width = 18
			panel.Height = 600

		if iType == "YZ":
			panel.Length = 18
			panel.Width = 600
			panel.Height = 300

		if iType == "ZY":
			panel.Length = 18
			panel.Width = 300
			panel.Height = 600

		FreeCAD.activeDocument().recompute()
	
	except:
	
		info = ""
		
		info += translate('panelDefaultInfo', 'This tool creates default panel that can be easily resized. You can clearly see where should be the thickness to keep exact panel XYZ axis orientation. All furniture elements should be created according to the XYZ axis plane, if possible. Avoid building whole furniture with rotated elements. If you want to rotate panel with dowels, better create panel with dowels without rotation, pack panel with dowels into LinkGroup, and use magicAngle to rotate whole LinkGroup. You can rotate whole furniture like this with single click.')

		showInfo("panelDefault"+iType, info)


# ###################################################################################################################
def panelCopy(iType):
	'''
	panelCopy(iType) - allows to copy selected panel into exact direction (iType).

	Note: This function displays pop-up info in case of error.

	Args:

		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"

	Usage:

		import MagicPanels
		
		MagicPanels.panelCopy("XY")
		
	Result:

		Created panel with correct direction XY.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]

		
		[ Length, Width, Height ] = sizesToCubePanel(gObj, iType)
		
		panel = FreeCAD.activeDocument().addObject("Part::Box", "panel"+iType)
		[ panel.Length, panel.Width, panel.Height ] = [ Length, Width, Height ]
		
		FreeCAD.activeDocument().recompute()

	except:

		info = ""
		
		info += translate('panelCopyInfo', 'This tool copy selected panel into exact XYZ axis orientation. By default you can copy any panel based on Cube object. If you want to copy Pad, you need to have Constraints named "SizeX" and "SizeY" at the Sketch. For other object types you need to have Length, Width, Height properties at object (Group: "Base", Type: "App::PropertyLength").') 

		showInfo("panelCopy"+iType, info)


# ###################################################################################################################
def panelMove(iType):
	'''
	panelMove(iType) - allows to move panel in given direction.

	Note: This function displays pop-up info in case of error.

	Args:
	
		iType: "Xp", "Xm", "Yp", "Ym", "Zp", "Zm"
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelMove("Xp")
		
	Result:
	
		Panel will be moved into X+ direction for 0 key view position. 
		If user rotated 3D model this should adjust to the model position.
		
	'''

	try:

		gObj = getReference()

		sizes = []
		sizes = getSizes(gObj)
		sizes.sort()

		x = 0
		y = 0
		z = 0
		
		if iType == "Xp":
			x = sizes[0]
		
		if iType == "Xm":
			x = - sizes[0]

		if iType == "Yp":
			y = sizes[0]

		if iType == "Ym":
			y = - sizes[0]

		if iType == "Zp":
			z = sizes[0]

		if iType == "Zm":
			z = - sizes[0]

		[ x, y, z ] = convertPosition(gObj, x, y, z)
		[ x, y, z ] = getModelRotation(x, y, z)

		[ px, py, pz, r ] = getPlacement(gObj)
		setPlacement(gObj, px+x, py+y, pz+z, r)

		FreeCAD.activeDocument().recompute()
	
	except:
		
		info = ""
		
		info += translate('panelMoveInfo', 'With the arrows you can quickly move Cube panels or even any other objects. If the thickness of the selected object can be recognized, the move step will be the thickness. So, you can solve common furniture problem with thickness offset. If the thickness will not be recognized the step will be 100. This allow you to move whole furniture segments very quickly. The arrows recognize the view model rotation. If you want precisely move object, use magicMove tool, instead. ')
		
		showInfo("panelMove"+iType, info)


# ###################################################################################################################
def panelMove2Face():
	'''
	panelMove2Face - allows to move panel to the face

	Note: This function displays pop-up info in case of error.

	Args:
	
		no args
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelMove2Face()
		
	Result:
	
		Panel will be moved to the face position.
		
	'''

	try:
	
		objects = FreeCADGui.Selection.getSelection()
		
		if len(objects) < 2:
			raise
		
		i = 0
		for o in objects:
			
			i = i + 1
			
			if i == 1:

				gObj = FreeCADGui.Selection.getSelection()[0]
				gFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

				gFPlane = getFacePlane(gFace)
				[ v1, v2, v3, v4 ] = getFaceVertices(gFace)

				continue
			
			obj = getReference(o)
			
			[ x, y, z, r ] = getPlacement(obj)
			
			if gFPlane == "XY":
				X = x
				Y = y
				Z = v1[2]
				R = r
				
			if gFPlane == "XZ":
				X = x
				Y = v1[1]
				Z = z
				R = r
			
			if gFPlane == "YZ":
				X = v1[0]
				Y = y
				Z = z
				R = r
			
			setPlacement(obj, X, Y, Z, R)
			FreeCAD.activeDocument().recompute()
			
	except:
		
		info = ""

		info += translate('panelMove2FaceInfo', 'This tool allows to align panels or any other objects to face position. First select face and next select objects you want to align with face position. You can select objects at objects Tree window holding left CTRL key. This tool allows to avoid thickness step problem, if you want to move panel to the other edge but the way is not a multiple of the panel thickness.')
		
		showInfo("panelMove2Face", info)
	

# ###################################################################################################################
def panelResize(iType):
	'''
	panelResize(iType) - allows to resize panel in given direction.
	
	Note: This function displays pop-up info in case of error.
	
	Args:
	
		iType 1: make bigger long side of panel
		iType 2: make smaller long side of panel
		iType 3: make bigger short side of panel
		iType 4: make smaller short side of panel
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelResize("1")
		
	Result:
	
		Make bigger long side of panel.
	'''

	try:

		gObj = getReference()

		sizes = []
		sizes = getSizes(gObj)
		sizes.sort()
		thick = sizes[0]

		if gObj.isDerivedFrom("Part::Box"):

			if iType == "1":
				if gObj.Length.Value == sizes[2]:
					gObj.Length = gObj.Length.Value + thick
					return
					
				if gObj.Width.Value == sizes[2]:
					gObj.Width = gObj.Width.Value + thick
					return
					
				if gObj.Height.Value == sizes[2]:
					gObj.Height = gObj.Height.Value + thick
					return

			if iType == "2":
				if gObj.Length.Value == sizes[2]:
					if gObj.Length.Value - thick > 0:
						gObj.Length = gObj.Length.Value - thick
					return
					
				if gObj.Width.Value == sizes[2]:
					if gObj.Width.Value - thick > 0:
						gObj.Width = gObj.Width.Value - thick
					return
					
				if gObj.Height.Value == sizes[2]:
					if gObj.Height.Value - thick > 0:
						gObj.Height = gObj.Height.Value - thick
					return

			if iType == "3":
				if gObj.Length.Value == sizes[1]:
					gObj.Length = gObj.Length.Value + thick
					return
					
				if gObj.Width.Value == sizes[1]:
					gObj.Width = gObj.Width.Value + thick
					return
					
				if gObj.Height.Value == sizes[1]:
					gObj.Height = gObj.Height.Value + thick
					return

			if iType == "4":
				if gObj.Length.Value == sizes[1]:
					if gObj.Length.Value - thick > 0:
						gObj.Length = gObj.Length.Value - thick
					return
					
				if gObj.Width.Value == sizes[1]:
					if gObj.Width.Value - thick > 0:
						gObj.Width = gObj.Width.Value - thick
					return
					
				if gObj.Height.Value == sizes[1]:
					if gObj.Height.Value - thick > 0:
						gObj.Height = gObj.Height.Value - thick
					return

		else:
		
			direction = getDirection(gObj)
		
			if iType == "1":
				
				if direction == "XY" or direction == "XZ" or direction == "YZ":
					gObj.Profile[0].setDatum(9, FreeCAD.Units.Quantity(sizes[2] + thick))
				else:
					gObj.Profile[0].setDatum(10, FreeCAD.Units.Quantity(sizes[2] + thick))
		
			if sizes[2] - thick > 0:

				if iType == "2":
				
					if direction == "XY" or direction == "XZ" or direction == "YZ":
						gObj.Profile[0].setDatum(9, FreeCAD.Units.Quantity(sizes[2] - thick))
					else:
						gObj.Profile[0].setDatum(10, FreeCAD.Units.Quantity(sizes[2] - thick))

			if iType == "3":
				
				if direction == "XY" or direction == "XZ" or direction == "YZ":
					gObj.Profile[0].setDatum(10, FreeCAD.Units.Quantity(sizes[1] + thick))
				else:
					gObj.Profile[0].setDatum(9, FreeCAD.Units.Quantity(sizes[1] + thick))

			if sizes[1] - thick > 0:
				
				if iType == "4":
				
					if direction == "XY" or direction == "XZ" or direction == "YZ":
						gObj.Profile[0].setDatum(10, FreeCAD.Units.Quantity(sizes[1] - thick))
					else:
						gObj.Profile[0].setDatum(9, FreeCAD.Units.Quantity(sizes[1] - thick))

		FreeCAD.activeDocument().recompute()

	except:
		
		info = ""
		
		info += translate('panelResizeInfo', 'This tool allows to resize quickly Cube panels or even other objects. The resize step is the panel thickness. Panel is resized into direction described by the icon for XY panel. However, in some cases the panel may be resized into opposite direction, if the panel is not supported or the sides are equal.')
		
		showInfo("panelResize"+iType, info)


# ###################################################################################################################
def panelFace(iType):
	'''
	panelFace(iType) - allows to create simple panel based on selected face and object.

	Note: This function displays pop-up info in case of error.
	
	Args:
	
		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelFace("XY")
		
	Result:
	
		Created panel at selected face with correct placement.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]
		gFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelFace"+iType)
		[ panel.Length, panel.Width, panel.Height ] = sizesToCubePanel(gObj, iType)

		if gObj.isDerivedFrom("Part::Box"):
			[ x, y, z ] = getVertex(gFace, 0, 1)
		else:
			[ x, y, z ] = getVertex(gFace, 1, 0)

		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
		FreeCAD.activeDocument().recompute()
		
	except:
		
		info = ""
		
		info += translate('panelFaceInfo', 'This tool creates new panel at selected face. The blue panel represents the selected object and the red one represents the new created object. The icon refers to base XY model view (0 key position). Click fitModel to set model into referred view. If you have problem with unpredicted result, use magicManager tool to preview panel before creation.')

		showInfo("panelFace"+iType, info)


# ###################################################################################################################
def panelBetween(iType):
	'''
	panelBetween(iType) - allows to create simple panel between 2 selected faces.
	
	Note: This function displays pop-up info in case of error.
	
	Args:
	
		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelBetween("XY")
		
	Result:
	
		Created panel between 2 selected faces with correct placement.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]
		gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
	
		[ x1, y1, z1 ] = getVertex(gFace1, 0, 1)
		[ x2, y2, z2 ] = getVertex(gFace2, 0, 1)

		x = abs(x2 - x1)
		y = abs(y2 - y1)
		z = abs(z2 - z1)

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelBetween"+iType)
		[ panel.Length, panel.Width, panel.Height ] = sizesToCubePanel(gObj, iType)

		z1 = z1 + gObj.Height.Value - panel.Height.Value
		
		if x > 0:
			panel.Length = x
		
		if y > 0:
			panel.Width = y
			
		if z > 0:
			panel.Height = z

		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z1), FreeCAD.Rotation(0, 0, 0))
		FreeCAD.activeDocument().recompute()

	except:
		
		info = ""
		
		info += translate('panelBetweenInfo', 'This tool creates new panel between two selected faces. Selection faces order is important. To select more than one face, hold left CTRL key during second face selection. The blue panels represents the selected objects and the red one represents the new created object. The icon refers to base XY model view (0 key position). Click fitModel to set model into referred view. If you have problem with unpredicted result, use magicManager tool to preview panel before creation.')

		showInfo("panelBetween"+iType, info)


# ###################################################################################################################
def panelSide(iType):
	'''
	panelSide(iType) - allows to create back of the furniture with 3 selected faces.
	
	Note: This function displays pop-up info in case of error.
	
	Args:
	
		"1": Left side of the furniture
		"2": Left side of the furniture but raised up
		"3": Right side of the furniture
		"4": Right side of the furniture but raised up
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelSide("1")
		
	Result:
	
		Created side of the furniture.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]
		gFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

		[ Length, Width, Height ] = sizesToCubePanel(gObj, "ZY")

		if gObj.isDerivedFrom("Part::Box"):
			[ x, y, z ] = getVertex(gFace, 0, 1)

		else:

			if iType == "1" or iType == "2":
				[ x, y, z ] = getVertex(gFace, 0, 0)

			if iType == "3" or iType == "4":
				[ x, y, z ] = getVertex(gFace, 1, 0)

		if iType == "1":
			x = x - Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideLeft")
		
		if iType == "2":
			z = z + Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideLeftUP")
		
		if iType == "3":
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideRight")
		
		if iType == "4":
			x = x - Length
			z = z + Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideRightUP")

		panel.Length = Length
		panel.Width = Width
		panel.Height = Height
		
		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
		FreeCAD.activeDocument().recompute()

	except:
		
		info = ""
		
		info += translate('panelSideInfo', 'This tool creates new panel at selected face. The blue panel represents the selected object and the red one represents the new created object. The arrow describe if the panel will be created up or down. The icon refers to base XY model view (0 key position). Click fitModel to set model into referred view. If you have problem with unpredicted result, use magicManager tool to preview panel before creation.')

		if iType == "1":
			showInfo("panelSideLeft", info)
		if iType == "2":
			showInfo("panelSideLeftUP", info)
		if iType == "3":
			showInfo("panelSideRight", info)
		if iType == "4":
			showInfo("panelSideRightUP", info)


# ###################################################################################################################
def panelBackOut():
	'''
	panelCover(iType) - allows to create back of the furniture with 3 selected faces.
	
	Note: This function displays pop-up info in case of error.
	
	Args:
	
		no args
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelBackOut()
		
	Result:
	
		Created back of the furniture.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]

		gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
		gFace3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]

		[ x, y, z ] = sizesToCubePanel(gObj, "ZX")

		[ x1, y1, z1 ] = getVertex(gFace1, 0, 1)
		[ x2, y2, z2 ] = getVertex(gFace2, 0, 0)
		[ x3, y3, z3 ] = getVertex(gFace3, 0, 1)

		x = abs(x2 - x1)
		z = z - z3

		if x > 0 and y > 0 and z > 0:

			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelBackOut")
			panel.Length = x
			panel.Width = y
			panel.Height = z

			panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z3), FreeCAD.Rotation(0, 0, 0))
			FreeCAD.activeDocument().recompute()
			
		else:
		
			raise
			
	except:
			
		info = ""
		
		info += translate('panelBackOutInfo', 'This tool allows to create back of the furniture with single click. To create back of the furniture you have to select 3 faces in the order described by the icon. To select more than one face, hold left CTRL key during face selection. The red edges at blue panels represents the selected faces. The transparent red panel represents the new created object. The icon refers to the back of the furniture.')
		
		showInfo("panelBackOut", info)


# ###################################################################################################################
def panelCover(iType):
	'''
	panelCover(iType) - allows to create simple panel on top of 3 selected faces.
	
	Note: This function displays pop-up info in case of error.
	
	Args:
	
		iType: "XY", "YX", "XZ", "ZX", "YZ", "ZY"
	
	Usage:
	
		import MagicPanels
		
		MagicPanels.panelCover("XY")
		
	Result:
	
		Created panel on top of 3 selected faces with correct placement.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]
		
		gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
		gFace3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]

		[ x, y, z ] = sizesToCubePanel(gObj, iType)

		[ x1, y1, z1 ] = getVertex(gFace1, 0, 1)
		[ x2, y2, z2 ] = getVertex(gFace2, 2, 1)
		[ x3, y3, z3 ] = getVertex(gFace3, 0, 1)

		x = abs(x2 - x1)
		y = y + z

		if x > 0 and y > 0 and z > 0:
		
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelCover"+iType)
			panel.Length = x
			panel.Width = y
			panel.Height = z

			panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z3), FreeCAD.Rotation(0, 0, 0))
			FreeCAD.activeDocument().recompute()

	except:
		
		info = ""
		
		info += translate('panelCoverInfo', 'This tool allows to create top cover of the furniture with single click. To create top cover of the furniture you have to select 3 faces in the order described by the icon. To select more than one face, hold left CTRL key during face selection. The red edges at blue panels represents the selected faces. The transparent red panel represents the new created object. The icon refers to the base XY model view (0 key position). Click fitModel to set model into referred view.')

		showInfo("panelCover"+iType, info)


# ###################################################################################################################
def panel2pad(iLabel="panel2pad"):
	'''
	panel2pad() - allows to replace Cube panel with the same panel but Pad.

	Note: This function displays pop-up info in case of error.
	
	Args:

		iLabel (optional): name all parts with given string

	Usage:

		import MagicPanels
		
		MagicPanels.panel2pad()
		
	Result:

		Selected Cube panel will be replaced with Pad and return [ part, body, sketch, pad ] references 
		that can be used for further transformations.
	'''

	try:

		gObj = FreeCADGui.Selection.getSelection()[0]

		[ part, body, sketch, pad ] = makePad(gObj, iLabel)
		
		FreeCAD.ActiveDocument.removeObject(gObj.Name)
		FreeCAD.activeDocument().recompute()
		
		return [ part, body, sketch, pad ]

	except:
		
		info = ""
		
		info += translate('panel2padInfo', 'This tool allows to replace Cube panel with Pad panel. The new created Pad panel will get the same dimensions, placement and rotation as the selected Cube panel. You can transform only one Cube panel into Pad at once. This tool is mostly dedicated to add decoration that is not supported for Cube objects by FreeCAD PartDesign workbench. You can also change shape by changing the Sketch.')
	
		showInfo("panel2pad", info)
	

# ###################################################################################################################
def panel2profile():
	'''
	panel2profile() - allows to replace Cube panels with construction profiles made from Thickness.

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		
		profiles = MagicPanels.panel2profile()
		
	Result:

		Selected Cube panels will be changed into Thickness construction profiles. This function 
		returns array with references to the created profiles, so it can be used for further 
		transfomrations.
	'''

	try:

		profiles = []
		objects = FreeCADGui.Selection.getSelection()
		if len(objects) == 0:
			raise
			
		for gObj in objects:
		
			sizes = getSizes(gObj)
			sizes.sort()
			if sizes[0] != sizes[1]:
				raise
			
			[ part, body, sketch, pad ] = makePad(gObj, "Construction")
			FreeCAD.ActiveDocument.removeObject(gObj.Name)
			FreeCAD.activeDocument().recompute()
			
			profile = body.newObject('PartDesign::Thickness','Profile')
			
			faces = []
			i = 0
			for f in pad.Shape.Faces:
				if int(round(pad.Shape.Faces[i].Length)) == int(round(4 * sizes[0])):
					faces.append("Face"+str(i+1))

				i = i + 1
				
			profile.Base = (pad, faces)
			profile.Value = 1
			profile.Reversed = 1
			profile.Mode = 0
			profile.Intersection = 0
			profile.Join = 0

			pad.Visibility = False

			FreeCAD.activeDocument().recompute()
			
			colors = [ (0.0, 0.0, 0.0, 0.0),
				(0.0, 0.0, 0.0, 0.0),
				(0.0, 0.0, 0.0, 0.0),
				(0.0, 0.0, 0.0, 0.0),
				(0.0, 0.0, 0.0, 0.0),
				(0.0, 1.0, 0.0, 0.0),
				(0.0, 0.0, 0.0, 0.0),
				(0.0, 1.0, 0.0, 0.0),
				(0.0, 1.0, 0.0, 0.0),
				(0.0, 1.0, 0.0, 0.0) ]

			profile.ViewObject.DiffuseColor = colors

			FreeCAD.activeDocument().recompute()
			profiles.append(profile)
		
		return profiles
	
	except:
		
		info = ""
		
		info += translate('panel2profileInfo', 'This tool allows to replace Cube panel with construction profile. You can replace more than one Cube panel at once. To select more objects hold left CTRL key during selection. The selected Cube objects need to have two equal sizes e.g. 20 mm x 20 mm x 300 mm to replace it with construction profile. The new created construction profile will get the same dimensions, placement and rotation as the selected Cube panel. If you have all construction created with simple Cube objects that imitating profiles, you can replace all of them with realistic looking construction profiles with single click.')
	
		showInfo("panel2profile", info)


# ###################################################################################################################
def panel2frame():
	'''
	panel2frame() - allows to replace Cube panels with frame elements cut with 45 angle. You have to select 
	face at Cube panels to make frame.

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		
		frames = MagicPanels.panel2frame()
		
	Result:

		Selected Cube panels faces will be changed into frame. This function 
		returns array with references to the created frames, so it can be used for further 
		transfomrations.
	'''

	try:

		frames = []
		frame = ""
		objects = FreeCADGui.Selection.getSelection()
		
		if len(objects) == 0:
			raise
		
		faces = dict()
		
		i = 0
		for o in objects:
			faces[o] = FreeCADGui.Selection.getSelectionEx()[i].SubObjects
			i = i + 1

		for o in objects:
			
			face = faces[o][0]
		
			sizes = getSizes(o)
			sizes.sort()
			
			[ faceType, arrAll, arrThick, arrShort, arrLong ] = getFaceEdges(o, face)
			
			keys = []
			
			if faceType == "edge":
				arr = arrThick
				size = sizes[1]
			if faceType == "surface":
				arr = arrShort
				size = sizes[0]
				
			for e in arr:
				keys.append(str(e.BoundBox))
			
			[ part, body, sketch, pad ] = makePad(o, "Frame")
			FreeCAD.ActiveDocument.removeObject(o.Name)
			FreeCAD.activeDocument().recompute()
		
			edges = []
			for k in keys:
				index = getEdgeIndexByKey(pad, k)
				edges.append("Edge"+str(int(index)))
			
			frame = body.newObject('PartDesign::Chamfer','Frame45Cut')
			frame.Base = (pad, edges)
			frame.Size = size - 0.01
			pad.Visibility = False
			
			FreeCAD.activeDocument().recompute()
			
			color = (0.5098039507865906, 0.3137255012989044, 0.1568627506494522, 0.0)

			frame.ViewObject.ShapeColor = color
			frame.ViewObject.DiffuseColor = color
			FreeCAD.activeDocument().recompute()
			
			frames.append(frame)
		
		return frames
	
	except:
		
		info = ""
		
		info += translate('panel2frameInfo', 'This tool allows to replace Cube panel with frame 45 cut at both sides. You can replace more than one Cube panel at once. To replace Cube objects with frames you have to select exact face at each Cube object. To select more objects hold left CTRL key during selection. The new created frame will get the same dimensions, placement and rotation as the selected Cube panel but will be cut at the selected face. If you have all construction created with simple Cube objects that imitating picture frame or window, you can replace all of them with realistic looking frame with single click.')

		showInfo("panel2frame", info)


# ###################################################################################################################
def panel2link():
	'''
	panel2link() - allows to replace Cube panels with Link. You have to select at least 2 objects. 
	First object will be the base object, and all others will be replaced with Link.

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		
		frames = MagicPanels.panel2link()
		
	Result:

		Selected detailed Screw and Dowels made from Cylinder, should result replace all simple Cylinder dowels, 
		with detailed Screw. 
	'''

	try:

		links = []
		objects = FreeCADGui.Selection.getSelection()
		
		if len(objects) < 2:
			raise
		
		i = 0
		for o in objects:
			
			i = i + 1
			
			if i == 1:
				base = o
				continue
			
			linkName = "Link_" + str(o.Name)
			link = FreeCAD.activeDocument().addObject('App::Link', linkName)
			link.setLink(base)
			link.Label = "Link, " + o.Label
			
			[ x, y, z, r ] = getPlacement(o)
			setPlacement(link, x, y, z, r)
			
			FreeCAD.ActiveDocument.removeObject(str(o.Name))
			FreeCAD.activeDocument().recompute()
			
			links.append(link)
			
			
		return links
	
	except:
		
		info = ""
		
		info += translate('panel2linkInfo', 'This tool allows to replace simple objects with any detailed object, e.g. Cylinder with realistic looking dowel made with Pad. First you have to select detailed object and than simple object that will be replaced with Link. The first selected detailed object can be Part, LinkGroup or any other created manually or merged with your project. You can replace more than one simple objects at once with Link. To select more objects hold left CTRL key during selection. The simple objects should imitate the detailed object to replace all of them in-place with realistic looking one. ')

		info += translate('panel2linkInfo', 'For more details please see:')
		info += ' ' + '<a href="https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture">'
		info += translate('panel2linkInfo', 'fixture.')
		info += '</a>'

		showInfo("panel2link", info)


# ###################################################################################################################
def drillHoles():
	'''
	drillHole() - allows to drill holes in selected face below selected cylinders.
	First object will be the base object face, and all others should be cylinders to drill holes.

	Note: This function displays pop-up info in case of error.

	Args:
		
		no args
		
	Usage:

		import MagicPanels
		holes = MagicPanels.drillHoles()
		
	Result:

		Selected face will be drilled below selected cylinders. 
		If the first selected object is Cube it will be changed into Pad. 
	'''

	try:

		import Part, Sketcher

		base = FreeCADGui.Selection.getSelection()[0]
		face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		objects = FreeCADGui.Selection.getSelection()
		
		del objects[0]
			
		# if face is selected create drill bit at face only
		if len(objects) == 0:

			d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DrillBitHole")
			d.Label = "Drill Bit - simple hole "

			# default drill bit size
			d.Radius = 4
			d.Height = 25

			# default drill bit position 0 - vertex
			[ v1, v2, v3, v4 ] = getFaceVertices(face)
			x, y, z = v1[0], v1[1], v1[2]
			
			r = getFaceObjectRotation(base, face)
			
			setPlacement(d, x, y, z, r)
			
			# default drill bit colors (middle, bottom, top)
			colors = [ (1.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0) ]
			d.ViewObject.DiffuseColor = colors
			
			return

		makeHoles(base, face, objects)
	
	except:
		
		info = ""
		
		info += translate('drillHoles', 'This is drill bit to make simple hole. The hole will be drilled below the bottom part of the drill bit, below the red face of the cylinder. The radius and depth of the hole will be the same as drill bit radius and height. You can resize the drill bit if you want. If you select face only, the drill bit will be created in the corner of the face (0 vertex). So, you will be able to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face to get exact hole depth. If you select face and than any amount of drill bits, the holes will be drilled below each drill bit. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad.')

		showInfo("drillHoles", info)


# ###################################################################################################################
def drillCountersinks():
	'''
	drillCountersinks() - allows to drill hole with countersink in selected face below selected drill bit. 
	First object will be the base object face, and all others should be drill bits 
	to drill holes with countersinks.

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		holes = MagicPanels.drillCountersinks()
		
	Result:

		Selected face will be drilled below selected drill bits. 
		If the first selected object is Cube it will be changed into Pad. 
	'''

	try:

		import Part, Sketcher

		holes = []

		base = FreeCADGui.Selection.getSelection()[0]
		face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		objects = FreeCADGui.Selection.getSelection()
		
		del objects[0]

		# if face is selected create drill bit at face only
		if len(objects) == 0:
			
			d = FreeCAD.ActiveDocument.addObject("Part::Cone","DrillBitCountersink")
			d.Label = "Drill Bit - countersink "

			# default drill bit size
			d.Radius1 = 2
			d.Radius2 = 5
			d.Height = 50

			# default drill bit position 0 - vertex
			[ v1, v2, v3, v4 ] = getFaceVertices(face)
			x, y, z = v1[0], v1[1], v1[2]
			
			r = getFaceObjectRotation(base, face)
			
			setPlacement(d, x, y, z, r)
			
			# default drill bit colors (middle, bottom, top)
			colors = [ (0.0, 1.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ]
			d.ViewObject.DiffuseColor = colors
			
			return
		
		makeCountersinks(base, face, objects)
	
	except:
		
		info = ""
		
		info += translate('drillCountersinks', 'This is drill bit to make countersink with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of countersink will be drill bit Radius2. The hole depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad.')

		showInfo("drillCountersinks", info)
	

# ###################################################################################################################
def drillCounterbores():
	'''
	drillCounterbores() - allows to drill hole with counterbore in selected face below selected drill bits. 
	First object will be the base object face, and all others should be drill bits to drill 
	holes with counterbores.

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		holes = MagicPanels.drillCounterbores()
		
	Result:

		Selected face will be drilled below selected drill bits. 
		If the first selected object is Cube it will be changed into Pad. 
	'''

	try:

		import Part, Sketcher

		holes = []

		base = FreeCADGui.Selection.getSelection()[0]
		face = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		objects = FreeCADGui.Selection.getSelection()
		
		del objects[0]

		# if face is selected create drill bit at face only
		if len(objects) == 0:
	
			d = FreeCAD.ActiveDocument.addObject("Part::Cone","DrillBitCounterbore")
			d.Label = "Drill Bit - counterbore "

			# default drill bit size
			d.Radius1 = 3
			d.Radius2 = 7.5
			d.Height = 50
			
			# default drill bit position 0 - vertex
			[ v1, v2, v3, v4 ] = getFaceVertices(face)
			x, y, z = v1[0], v1[1], v1[2]
			
			r = getFaceObjectRotation(base, face)
			
			setPlacement(d, x, y, z, r)
			
			# default drill bit colors (middle, bottom, top)
			colors = [ (0.0, 0.0, 1.0, 0.0), (0.0, 1.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0) ]
			d.ViewObject.DiffuseColor = colors

			return
		
		makeCounterbores(base, face, objects)
	
	except:
		
		info = ""
		
		info += translate('drillCounterbores', 'This is drill bit to make counterbore with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of counterbore will be drill bit Radius2. The hole depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad.')

		showInfo("drillCounterbores", info)


# ###################################################################################################################
def sketch2dowel():
	'''
	sketch2dowel() - allows to create dowel above the selected Sketch of the hole. The dowels size will be taken from
	hole object. The position will be taken from selected Sketch.

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		
		holes = MagicPanels.sketch2dowel()
		
	Result:

		The dowel will be created above the selected Sketch, at the hole object surface.
	'''

	try:
	
		objects = FreeCADGui.Selection.getSelection()

		if len(objects) != 2:
			raise
		
		sketch = FreeCADGui.Selection.getSelection()[0]
		face = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
		
		if not sketch.isDerivedFrom("Sketcher::SketchObject"):
			raise
			
		hole = ""
			
		if sketch.InList[0].isDerivedFrom("PartDesign::Hole"):
			hole = sketch.InList[0]
			
		if sketch.InList[1].isDerivedFrom("PartDesign::Hole"):
			hole = sketch.InList[1]
			
		if hole == "":
			raise
				
		x = sketch.Placement.Base.x
		y = sketch.Placement.Base.y
		z = sketch.Placement.Base.z
		r = getFaceObjectRotation(hole, face)
			
		d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DowelSketch")
		d.Label = "Dowel - " + str(sketch.Label)

		d.Radius = hole.Diameter / 2
		d.Height = hole.Depth

		setPlacement(d, x, y, z, r)

		return d

	except:
		
		info = ""
		
		info += translate('sketch2dowel', 'This tool allows to create dowel at the selected hole. To create dowel select Sketch for the hole and face of the hole object. The dowel position will be get from the Sketch and the face refer to the side the dowel will be raised. The dowel radius and height will be get from hole object. If the hole is throughAll the dowel height will be very big, so make sure you use dimensions instead for hole. To select more objects hold left CTRL key during selection.')

		showInfo("sketch2dowel", info)


# ###################################################################################################################
def edge2dowel():
	'''
	edge2dowel() - allows to create dowels above the selected edge of the hole. The dowels size and placement 
	will be taken from edge circle curve.

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		
		dowels = MagicPanels.edge2dowel()
		
	Result:

		The dowels will be created above the selected hole edges.
	'''

	try:

		dowels = []
		objects = FreeCADGui.Selection.getSelectionEx()[0].SubObjects

		if len(objects) == 0:
			raise
		
		for e in objects:
		
			if not e.Curve.isDerivedFrom("Part::GeomCircle"):
				raise
			
			edgeRadius = e.Curve.Radius
			x = e.Curve.Center[0]
			y = e.Curve.Center[1]
			z = e.Curve.Center[2]
			r = e.Curve.Rotation
			
			d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DowelEdge")
			d.Label = "Dowel - edge "

			d.Radius = edgeRadius
			d.Height = 40

			setPlacement(d, x, y, z, r)

			dowels.append(d)

		return dowels
			
	except:
		
		info = ""
		
		info += translate('edge2dowel', 'This tool allows to create dowels above the selected hole edges. To create dowel select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The dowel Height will be 40. The dowel radius will be get from the selected edge hole radius. To select more objects hold left CTRL key during selection.')

		showInfo("edge2dowel", info)


# ###################################################################################################################
def edge2drillbit():
	'''
	edge2drillbit() - allows to create drillbits above the selected edge of the hole. The drillbits size and placement 
	will be taken from edge circle curve.

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		
		drillbits = MagicPanels.edge2drillbit()
		
	Result:

		The drillbits will be created above the selected hole edges.
	'''

	try:

		drillbits = []
		objects = FreeCADGui.Selection.getSelectionEx()[0].SubObjects

		if len(objects) == 0:
			raise
		
		for e in objects:
		
			if not e.Curve.isDerivedFrom("Part::GeomCircle"):
				raise
			
			edgeRadius = e.Curve.Radius - 1
			x = e.Curve.Center[0]
			y = e.Curve.Center[1]
			z = e.Curve.Center[2]
			r = e.Curve.Rotation
			
			d = FreeCAD.ActiveDocument.addObject("Part::Cylinder","DrillBitHole")
			d.Label = "Drill Bit - simple hole "

			d.Radius = edgeRadius
			d.Height = 16

			setPlacement(d, x, y, z, r)
			
			# default drill bit colors (middle, bottom, top)
			colors = [ (1.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0) ]
			d.ViewObject.DiffuseColor = colors
			
			drillbits.append(d)

		return drillbits
			
	except:
		
		info = ""
		
		info += translate('edge2drillbit', 'This tool allows to create drill bits for making simple hole. The drill bits will be created above the selected hole edges. To create drill bits select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The drill bit Height will be 16. The drill bits radius will be get from the selected edge hole radius but will be little smaller, 1 mm, than the hole to make pilot hole. To select more objects hold left CTRL key during selection. This feature can be used to create drill bits above holes at hinges, angles or other fixture type.')

		showInfo("edge2drillbit", info)


# ###################################################################################################################
def magicCut():
	'''
	magicCut() - allows to create multi bool cut operation at selected objects. First selected object 
	should be the base element and all other selected will cut the base. The copies will be created for cut. 

	Note: This function displays pop-up info in case of error.

	Args:

		no args

	Usage:

		import MagicPanels
		
		cuts = MagicPanels.magicCut()
		
	Result:

		Array of cut objects will be returned.
	'''

	try:

		objects = FreeCADGui.Selection.getSelection()

		if len(objects) < 2:
			raise

		cuts = makeCuts(objects)
		FreeCADGui.Selection.clearSelection()
		
		return cuts
	
	except:
		
		info = ""
		
		info += translate('magicCut', 'This tool make multi bool cut operation at selected objects. First object should be the base object to cut. All other selected objects will cut the base 1st selected object. To select more objects hold left CTRL key during selection. During this process the objects copies will be used to cut and the original objects will be not be moved. Also there will be auto labeling to keep the cut tree more informative and cleaner.')

		showInfo("magicCut", info)


# ###################################################################################################################
