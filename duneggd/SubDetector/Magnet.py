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
    def configure(self, actDimension     =None, actDimensionB=None, magGap=None, magBGap=None,
                        actThickness =None, actThicknessB=None, Location=None,
		        actMaterial =None, actMaterialB=None, nMag=None, nMagB=None, **kwds):

        self.magInDim  = actDimension     
        self.magOutDim = list(actDimension)
        self.magOutDim[1] += 2*actThickness 
        self.magOutDim[2] += 2*actThickness
        self.MagMat = actMaterial 
        self.actThickness = actThickness
	self.location     = list(Location)

        self.magInDimB  = actDimensionB
        self.magInDimB = list(actDimensionB)
        self.magOutDimB = list(actDimensionB)
        self.magOutDimB[0] += 2*actThicknessB
        self.magOutDimB[1] += 2*actThicknessB
        self.MagMatB = actMaterialB
	self.nMag    = nMag
	self.nMagB   = nMagB
	self.magGap  = magGap
	self.magBGap = magBGap
     
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Make the scint bar shape and volume
        magOut = geom.shapes.Box( 'MagOut',                 dx=0.5*self.magOutDim[0], 
                                  dy=0.5*self.magOutDim[1], dz=0.5*self.magOutDim[2]) 
        magIn = geom.shapes.Box(  'MagInner',               dx=0.5*self.magInDim[0], 
                                  dy=0.5*self.magInDim[1],  dz=0.5*self.magInDim[2]) 

        magBox = geom.shapes.Boolean( 'Mag', type='subtraction', first=magOut, second=magIn ) 
        Mag_lv = geom.structure.Volume('volMag', material=self.MagMat, shape=magBox)

        magOutB = geom.shapes.Box( 'YokeOut',                 dx=0.5*self.magOutDimB[0],
                                  dy=0.5*self.magOutDimB[1], dz=0.5*self.magOutDimB[2])
        magInB = geom.shapes.Box(  'YokeInner',               dx=0.5*self.magInDimB[0],
                                  dy=0.5*self.magInDimB[1],  dz=0.5001*self.magOutDimB[2])

        magBoxB = geom.shapes.Boolean( 'Yoke', type='subtraction', first=magOutB, second=magInB )
        MagBlock_lv = geom.structure.Volume('volYoke', material=self.MagMatB, shape=magBoxB)

        magnetOut = geom.shapes.Box( 'MagnetOut',                 dx=0.5*self.magOutDimB[0],
                                  dy=0.5*self.magOutDimB[1], dz=0.5*self.magOutDim[2])
        magnetIn = geom.shapes.Box(  'MagnetInner',               dx=0.5*(self.magInDim[0]+self.magGap)*self.nMag,
                                  dy=0.5*self.magInDim[1],  dz=0.5*self.magInDim[2])

        magnetBox = geom.shapes.Boolean( 'Magnet', type='subtraction', first=magnetOut, second=magnetIn )
        Magnet_lv = geom.structure.Volume('volMagnet', 'Air', shape=magnetBox)

	#self.add_volume(Mag_lv)
	#self.add_volume(MagBlock_lv)
        self.add_volume(Magnet_lv)

        for i in range(self.nMag):
        	magPos  = geom.structure.Position( 'magPos-'+str(i)+'_in_'+self.name,
        	                                    self.location[0]-self.nMag*(self.magGap+self.magInDim[0])/2+(i+0.5)*self.magInDim[0]+i*self.magGap, self.location[1], self.location[2])
        	pMag = geom.structure.Placement( 'magPla-'+str(i)+'_in_'+self.name,
        	                                   volume = Mag_lv,pos = magPos)
        	Magnet_lv.placements.append( pMag.name )

        for j in range(self.nMagB):
                magBPos  = geom.structure.Position( 'magBPos-'+str(j)+'_in_'+self.name,
                                                    self.location[0], self.location[1], self.location[2]-self.nMagB*(self.magBGap+self.magInDimB[2])/2+(j+0.5)*self.magInDimB[2]+j*self.magBGap)
                pMagB = geom.structure.Placement( 'magBPla-'+str(j)+'_in_'+self.name,
                                                   volume = MagBlock_lv,pos = magBPos)
                Magnet_lv.placements.append( pMagB.name )

	return


