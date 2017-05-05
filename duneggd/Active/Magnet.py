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
    def configure(self, actDimension     =None, actDimensionB=None,
                        actThickness =None, actThicknessB=None, actSize=None, actGap=None,
		        actMaterial =None, actMaterialB=None, **kwds):

        self.magInDim  = actDimension     
        self.magOutDim = list(actDimension)
        self.magOutDim[1] += 2*actThickness 
        self.magOutDim[2] += 2*actThickness
        self.MagMat = actMaterial 
        self.actThickness = actThickness

        self.actGap = actGap
        self.magInDimB  = actDimensionB
        self.magInDimB = list(actDimensionB)
        #self.magInDimB[0] += actThickness
        #self.magInDimB[1] += actThickness
        #self.magInDimB[2] += actGap
        self.magOutDimB = list(actDimensionB)
        self.magOutDimB[0] += 2*actThicknessB
        self.magOutDimB[1] += 2*actThicknessB
        #self.magOutDimB[2] += 2*actThicknessB
        #self.magOutDimB[0] += actGap
        #self.magOutDimB[1] += actGap
        #self.magOutDimB[2] += actGap
        self.MagMatB = actMaterialB
     
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Make the scint bar shape and volume
        magOut = geom.shapes.Box( 'MagOut',                 dx=0.5*self.magOutDim[0], 
                                  dy=0.5*self.magOutDim[1], dz=0.5*self.magOutDim[2]) 
        magIn = geom.shapes.Box(  'MagInner',               dx=0.5*self.magInDim[0], 
                                  dy=0.5*self.magInDim[1],  dz=0.5*self.magInDim[2]) 

        magBox = geom.shapes.Boolean( 'Magnet', type='subtraction', first=magOut, second=magIn ) 
        Mag_lv = geom.structure.Volume('volMagnet', material=self.MagMat, shape=magBox)

        magOutB = geom.shapes.Box( 'YokeOut',                 dx=0.5*self.magOutDimB[0],
                                  dy=0.5*self.magOutDimB[1], dz=0.5*self.magOutDimB[2])
        magInB = geom.shapes.Box(  'YokeInner',               dx=0.5*self.magInDimB[0],
                                  dy=0.5*self.magInDimB[1],  dz=0.5*self.magInDimB[2])

        magBoxB = geom.shapes.Boolean( 'Yoke', type='subtraction', first=magOutB, second=magInB )
        MagBlock_lv = geom.structure.Volume('volYoke', material=self.MagMatB, shape=magBoxB)

        #magBPos  = geom.structure.Position( 'magBPos',
        #                                    Q('0m'), Q('0m'),  Q('0m'))
        #pMagB = geom.structure.Placement( 'placeMagB',
        #                                   volume = MagBlock_lv,pos = magBPos)
        #Mag_lv.placements.append( pMagB.name )

        self.add_volume(Mag_lv)
        self.add_volume(MagBlock_lv)

