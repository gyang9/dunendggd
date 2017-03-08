#!/usr/bin/env python
'''
Subbulder of STTBuilder
'''

import gegede.builder
from gegede import Quantity as Q
import math


class STBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, sTube_innerDia=None, sTube_outerDia=None, 
                  sTube_length=None, sAnodeWire_Dia=None,
                  stPlaneMat=None, strawMat=None, stGas=None, **kwds):
        self.material   = stPlaneMat
        self.strawMat   = strawMat
        self.stGas      = stGas
        self.sTube_innerDia = sTube_innerDia
        self.sTube_outerDia = sTube_outerDia
        self.sTube_length = sTube_length
        self.sAnodeWire_Dia = sAnodeWire_Dia


    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Make the straw tube shape and volume, and add straw into it
        # rmin=0, else material at 0 would be default of STPlane
        sTube      = geom.shapes.Tubs('StrawTube_'+self.name, 
                                      rmin = '0cm',                   
                                      rmax = 0.5*self.sTube_outerDia, 
                                      dz   = 0.5*self.sTube_length)
        sTube_lv   = geom.structure.Volume('volStrawTube_'+self.name, material=self.stGas, shape=sTube)
        straw      = geom.shapes.Tubs('Straw_'+self.name, 
                                      rmin = 0.5*self.sTube_innerDia, 
                                      rmax = 0.5*self.sTube_outerDia, 
                                      dz   = 0.5*self.sTube_length)
        straw_lv   = geom.structure.Volume('volStraw_'+self.name, material=self.strawMat, shape=straw)
        wire       = geom.shapes.Tubs('Wire_'+self.name,
                                       rmin = '0cm',
                                       rmax = 0.5*self.sAnodeWire_Dia,
                                       dz   = 0.5*self.sTube_length)
        wire_lv    = geom.structure.Volume('volWire_'+self.name, material=self.strawMat, shape=wire)

        pS_in_Tube = geom.structure.Placement( 'placeS_in_Tube_'+self.name, volume = straw_lv )
        pW_in_Tube = geom.structure.Placement( 'placeW_in_Tube_'+self.name, volume = wire_lv )
        sTube_lv.placements.append( pS_in_Tube.name )
        sTube_lv.placements.append( pW_in_Tube.name )
        self.add_volume(sTube_lv)
