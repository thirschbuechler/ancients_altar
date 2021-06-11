import vtk as vtk
import os

infile=""
while not os.path.isfile(infile):
    infile=input("please input infile: ")
outfile=infile+"_out.stl"

#https://gist.github.com/Hodapp87/8874941
def loadStl(fname):
    """Load the given STL file, and return a vtkPolyData object for it."""
    reader = vtk.vtkSTLReader()
    reader.SetFileName(fname)
    reader.Update()
    polydata = reader.GetOutput()
    return polydata

#https://stackoverflow.com/questions/64804792/how-to-make-an-open-stl-file-watertight
polydata = loadStl(infile)
input1 = vtk.vtkPolyData()
input1.DeepCopy(polydata)


# Append potentially multiple  meshes 
appendFilter = vtk.vtkAppendPolyData()

appendFilter.AddInputData(input1)

appendFilter.Update()

#  Remove any duplicate points.
cleanFilter = vtk.vtkCleanPolyData()
cleanFilter.SetInputConnection(appendFilter.GetOutputPort())
cleanFilter.Update()


# newData = cleanFilter

fill = vtk.vtkFillHolesFilter()
fill.SetInputConnection(appendFilter.GetOutputPort())   
fill.SetHoleSize(100)    
fill.Update()


stlWriter = vtk.vtkSTLWriter()
stlWriter.SetInputConnection(fill.GetOutputPort())
stlWriter.SetFileName(outfile)
stlWriter.Write()
