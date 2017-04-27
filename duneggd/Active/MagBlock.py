#!/usr/bin/env python
'''
Subbuilder of ECALBuilder
'''

import gegede.builder
from gegede import Quantity as Q
import math

class MagBlockBuilder(gegede.builder.Builder):
 
    # define builder data here
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, actDimension     =None,
                        actThickness =None, actSize=None, actMaterial =None, actSteel=None, **kwds):

        self.magInDim  = actDimension     
        self.magOutDim = list(actDimension)
        self.magOutDim[1] += 2*actThickness
        self.magOutDim[2] += 2*actThickness
        self.MagMat = actMaterial 
     
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Make the scint bar shape and volume
        magOut = geom.shapes.Box( 'MagOut',                 dx=0.5*self.magOutDim[0], 
                                  dy=0.5*self.magOutDim[1], dz=0.5*self.magOutDim[2]) 
        magIn = geom.shapes.Box(  'MagInner',               dx=0.5*self.magInDim[0], 
                                  dy=0.5*self.magInDim[1],  dz=0.5*self.magInDim[2]) 

        magBox = geom.shapes.Boolean( 'Magnet', type='subtraction', first=magOut, second=magIn ) 
        MagBlock_lv = geom.structure.Volume('volMagnet', material=self.MagMat, shape=magBox)

        self.add_volume(MagBlock_lv)

