#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 20:01:24 2021

@author: thomas
inspiration: https://pypi.org/project/numpy-stl/

Goal:
Make multiple blocks of different height in a 2D plane,
in a 3D space

"""
from stl import mesh # numpySTL
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
#import time #time.sleep blocks drawing sometimes


class ancients_altar(object):
# https://stargate.fandom.com/wiki/Ancient_control_panel

    def __init__(self):
        # initialize vars
        self.blocks=[]
        self.altar_field = np.NaN
        self.fig=[]
        self.vec_makeblock = np.vectorize(self.makeblock)
        self.vec_makeblockc = np.vectorize(self.makeblockc)
        
        
    def makeblockc(self,h=1,coord=[0,0]):
        self.makeblock(h=h,xpos=coord[0],ypos=coord[1])
    
    
    def makeblock(self,h=1,xpos=0,ypos=0):    
        # Create 3 faces of a cube
        data = np.zeros(6, dtype=mesh.Mesh.dtype)
        
        ## notes ##
        # - each vector defines a triangle
        # - look at which vectors coordinates are
        #       always 1 to figure out in wich plane it sits
        
        # Top of the cube
        data['vectors'][0] = np.array([[0, 1, h],
                                          [1, 0, h],
                                          [0, 0, h]])
        data['vectors'][1] = np.array([[1, 0, h],
                                          [0, 1, h],
                                          [1, 1, h]])
        # Front face
        data['vectors'][2] = np.array([[1, 0, 0],
                                          [1, 0, h],
                                          [1, 1, 0]])
        data['vectors'][3] = np.array([[1, 1, h],
                                          [1, 0, h],
                                          [1, 1, 0]])
        # Left face
        data['vectors'][4] = np.array([[0, 0, 0],
                                          [1, 0, 0],
                                          [1, 0, h]])
        data['vectors'][5] = np.array([[0, 0, 0],
                                          [0, 0, h],
                                          [1, 0, h]])
        
        # Since the cube faces are from 0 to 1 we can move it to the middle 
        #data['vectors'] -= .5 # would require z+= (h-1) on meshes_1 below
        
        # Generate 4 different meshes so we can rotate them later
        meshes = [mesh.Mesh(data.copy()) for _ in range(2)]
        
        # Rotate degrees over 2 axes to mirror
        meshes[1].rotate([1, 1, 0], np.pi)# 180°
        meshes[1].z += (h)
        
        combined = mesh.Mesh(np.concatenate([mesh.data for mesh in meshes]))
        
        combined.x += xpos
        combined.y += ypos
        
        self.blocks.append(combined)
        
        
    def make_mx_blocks(self, mx):
        xtrace=np.arange(0,np.shape(mx)[0])
        ytrace=np.arange(0,np.shape(mx)[1])
        coord = np.meshgrid(xtrace,ytrace)
        self.vec_makeblock(xpos=coord[0],ypos=coord[1], h=mx.T)
        
        
    def make_altar(self):
        self.altar_field = mesh.Mesh(np.concatenate([block.data for block in self.blocks])) # not ideal for same-sized blocks, but enables different sizes
        #todos
        #   - add frame
        #   - add labelling
        
        
    def show(self):
        self.make_altar()

        if not self.fig:
            self.fig = plt.figure()
        ax = mplot3d.Axes3D(self.fig)
        
        colors=["b","r","g"]
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(
                self.altar_field.vectors,facecolors=colors[0], linewidth=1, alpha=0.5))
        
        #ax.scatter(self.altar_field.x,self.altar_field.y,self.altar_field.z)#draw points

        # auto-scale to draw area - axes with equal lengths
        scale = np.concatenate(self.altar_field.points).flatten()
        ax.auto_scale_xyz(scale, scale, scale)

        # auto-scale to draw area - axes with different lengths        
        #xscale = np.concatenate(self.altar_field.x).flatten()
        #yscale = np.concatenate(self.altar_field.y).flatten()
        #zscale = np.concatenate(self.altar_field.z).flatten()
        #ax.auto_scale_xyz(xscale, yscale, zscale)
        
        # color axes
        ax.w_xaxis.line.set_color("red")
        ax.w_yaxis.line.set_color("green")
        ax.w_zaxis.line.set_color("blue")
        
        plt.show()
        
    def save(self, filename):
        if ".stl" not in filename:
            filename+=".stl"
        self.altar_field.save(filename) # and is slice-able in cura :)
        
    
    def makefield(self,xmax=5,ymax=10):#veery slow   
        for x in range(xmax):
                for y in range(ymax):
                    self.makeblock(xpos=x,ypos=y)
    
    
    def random_demo(self):#veery slow
        np.random.seed(42)
        for i,block in enumerate(self.blocks):
            #print("a")
            #print(block.z)
            z=block.z+ np.random.random()
            if (z>2).any():
                z=z-1
            self.blocks[i].z=z # change block z pos
            
            
    def random_demo_mx(self):#matrix access is fast
        #np.random.seed(42)#pseudo-random
        np.random.seed(int(time.time()))
        h=np.random.random(size=(5,10))
        self.make_mx_blocks(h) # different block heights
                
        
def demo1():
    aa = ancients_altar()
    aa.makeblock(h=0.5)
    aa.makeblock(xpos=1)
    aa.makeblock(xpos=4,h=2)
    aa.makeblock(xpos=0,ypos=2,h=6)
    aa.show()
    aa.save("demofield1")
    
    
def demo2():
    aa = ancients_altar()
    aa.makefield()#create blockfield
    aa.show()
    while True:
        aa.random_demo()#update blocks with rand values
        aa.show()
        #update and flush the same figure
        aa.fig.canvas.draw()
        aa.fig.canvas.flush_events()        
      
        
def demo2mx(): # abit faster
    aa = ancients_altar()
    while True:
        aa.random_demo_mx()#create blocks with rand values
        aa.show()
        #time.sleep(0.5)
        #update and flush the same figure
        aa.fig.canvas.draw()
        aa.fig.canvas.flush_events()  
        #time.sleep(0.1)
        aa.blocks=[]#flush blocks
        
        
def demo3():#vectorize externally
    aa = ancients_altar()
    va = np.vectorize(aa.makeblock)
    va(xpos=np.arange(1,10)) # vector input
    aa.show()
    

def demo4():#vectorize internally
    aa = ancients_altar()
    #va = np.vectorize(aa.makeblock)
    np.random.seed(42)
    l=10
    h=np.random.random(size=l)
    #va(xpos=np.arange(0,l),h=h)
    aa.vec_makeblock(xpos=np.arange(0,l),h=h)
    aa.show()
           
        
def demo5():#matrix externally, lxl
    aa = ancients_altar()
    np.random.seed(42)
    l=10
    h=np.random.random(size=(l,l))
    xpos=np.arange(0,l)
    ypos=xpos
    #aa.vec_makeblock(xpos=xpos,ypos=ypos, h=h)
    coord = np.meshgrid(xpos,ypos)
    print(coord[0])
    #aa.vec_makeblockc(coord=coord, h=h)
    aa.vec_makeblock(xpos=coord[0],ypos=coord[1], h=h)
    aa.show()
    
    
def demo6():#matrix internally, lxl
    aa = ancients_altar()
    
    # generate dummy matrix
    np.random.seed(42)
    l=10
    h=np.random.random(size=(l,l))
    
    aa.make_mx_blocks(h)
    aa.show()


def demo7():#matrix internally, mxn
    aa = ancients_altar()
    
    # generate dummy matrix
    np.random.seed(42)
    h=np.random.random(size=(5,10))
    
    aa.make_mx_blocks(h)
    aa.show()
    
        
#### test this library using semi Unit Testing ####
if __name__ == '__main__': # test if called as executable, not as library, regular prints allowed
   #demo1()
   #demo2()
   #demo3()
   #demo4()
   #demo5()
   #demo6()
   #demo7()
   demo2mx()
   pass#if no demo selected and just compiling in jupyter(e.g. spyder)  console to call later