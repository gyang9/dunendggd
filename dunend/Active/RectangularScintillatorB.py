#!/usr/bin/env python
'''
Subbuilder of ECALBuilder
'''

import gegede.builder
from gegede import Quantity as Q
import math

class SBBuilder(gegede.builder.Builder):
 
    # define builder data here
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, ScintBarDim= None,
                        ScintBarMat=None, **kwds):

        self.ScintBarMat = ScintBarMat
        self.ScintBarDim = ScintBarDim
     

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Make the scint bar shape and volume
        ScintBarBox = geom.shapes.Box('ScintBarBox',            dx=0.5*self.ScintBarDim[0], 
                                     dy=0.5*self.ScintBarDim[1], dz=0.5*self.ScintBarDim[2])
        ScintBar_lv = geom.structure.Volume('volScintBar', material=self.ScintBarMat, shape=ScintBarBox)
        self.add_volume(ScintBar_lv)

        return
