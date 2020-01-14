 #!/usr/bin/python
# -*- coding: utf-8 -*-
#****************************************************************************

import FreeCAD, FreeCADGui
import Draft
import PySide
from PySide import QtGui, QtCore

q_deflection = 0.005 #0.02 ##0.005
tol = 0.01
constr = 'coincident' #'all'

sel = FreeCADGui.Selection.getSelection()
if len(sel) != 1:
    reply = QtGui.QMessageBox.information(None,"Warning", "select one single object to be discretized")
    FreeCAD.Console.PrintError('select one single object to be discretized\n')
else:
    FreeCAD.ActiveDocument.openTransaction("Discretizing") #open a transaction for undo management
    shapes = []
    for selobj in sel:
        for e in selobj.Shape.Edges:
            shapes.append(Part.makePolygon(e.discretize(QuasiDeflection=q_deflection)))
    Draft.makeSketch(shapes)
    sk_d = FreeCAD.ActiveDocument.ActiveObject
    if sk_d is not None:
        FreeCADGui.ActiveDocument.getObject(sk_d.Name).LineColor = (1.00,1.00,1.00)
        FreeCADGui.ActiveDocument.getObject(sk_d.Name).PointColor = (1.00,1.00,1.00)
        max_geo_admitted = 1500 # after this number, no recompute is applied
        if len (sk_d.Geometry) < max_geo_admitted:
            FreeCAD.ActiveDocument.recompute()
    import constrainator
    constrainator.add_constraints(sk_d.Name, tol, constr)
    skt = FreeCAD.ActiveDocument.getObject(sk_d.Name)
    if hasattr(skt, 'OpenVertices'):
        openVtxs = skt.OpenVertices
        if len(openVtxs) >0:
            FreeCAD.Console.PrintError("Open Vertexes found.\n")
            FreeCAD.Console.PrintWarning(str(openVtxs)+'\n')
            msg = """Open Vertexes found.<br>"""+str(openVtxs)
            reply = QtGui.QMessageBox.information(None,"info", msg)
    FreeCADGui.ActiveDocument.getObject(sel[0].Name).Visibility=False
    FreeCAD.ActiveDocument.commitTransaction()
    