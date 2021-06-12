# ancients_altar
Make multiple blocks of different height in a 2D plane, in a 3D space

## plot and stl examples 
For example, some different heights and different positions

![demo1](Demo1.png)

or a plane of equal-sized cubes with a varying height

![demo2](Demo2.png)

## 3d printing

Can output 3d-printable STLs (confirmed slicing works in Cura 4.9 - results in valid toolpaths & infill)

Caveat: Slicing in Cura might take ages or forever on a slow CPU, as documented in slicing_tests.

## dependencies
python3, numpy, matplotlib, numpy-stl
