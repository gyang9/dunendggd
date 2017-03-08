#!/usr/bin/env python
'''
Subbuilder of ECALBuilder
'''

import gegede.builder
from gegede import Quantity as Q
import math

class MagnetBuilder(gegede.builder.Builder):
 
    # define builder data here
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, magInDim=None,
                        magThickness=None, MagMat=None, **kwds):

        self.magInDim  = magInDim
        self.magOutDim = list(magInDim)
        self.magOutDim[1] += 2*magThickness
        self.magOutDim[2] += 2*magThickness
        self.MagMat = MagMat 
     

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Make the scint bar shape and volume
        magOut = geom.shapes.Box( 'MagOut',                 dx=0.5*self.magOutDim[0], 
                                  dy=0.5*self.magOutDim[1], dz=0.5*self.magOutDim[2]) 
        magIn = geom.shapes.Box(  'MagInner',               dx=0.5*self.magInDim[0], 
                                  dy=0.5*self.magInDim[1],  dz=0.5*self.magInDim[2]) 

        magBox = geom.shapes.Boolean( 'Magnet', type='subtraction', first=magOut, second=magIn ) 
        Mag_lv = geom.structure.Volume('volMagnet', material=self.magMat, shape=magBox)
        self.add_volume(Mag_lv)


