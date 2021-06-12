#pymeshfix example for a shared-object linkage to meshfix
from pymeshfix import _meshfix
infile=input("please input infile: ")
outfile=infile+"_out.stl"
# Read mesh from infile and output cleaned mesh to outfile
_meshfix.clean_from_file(infile, outfile)
