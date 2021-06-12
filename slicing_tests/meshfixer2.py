#pymeshfix example for python operations
from pymeshfix import _meshfix
import pyvista as pv
import numpy as np


infile=input("please input infile: ")
outfile=infile+"_out.stl"
joiner=input("join? givebool!: ")

mesh = pv.read(infile)
vertices = np.asarray(mesh.points)
faces = np.asarray(mesh.faces).reshape((-1, 4))[:, 1:]



# Create TMesh object
tin = _meshfix.PyTMesh()


#tin.LoadFile(infile)#demo but does not work
tin.load_array(vertices, faces) # or read arrays from memory

# Attempt to join nearby components
if bool(joiner):
    tin.join_closest_components() # this takes a loong time

# Fill holes
tin.fill_small_boundaries()
print('There are {:d} boundaries'.format(tin.boundaries()))

# Clean (removes self intersections)
#tin.clean(max_iters=10, inner_loops=3) # this kills all struts and just leaves the center most

# Check mesh for holes again
print('There are {:d} boundaries'.format(tin.boundaries()))

# Clean again if necessary...

# Output mesh
tin.save_file(outfile)

 # or return numpy arrays
vclean, fclean = tin.return_arrays()
