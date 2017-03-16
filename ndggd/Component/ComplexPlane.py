#!/usr/bin/env python
'''
Subbulder of STTBuilder
'''

import gegede.builder
from gegede import Quantity as Q
import math


class STPlaneBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  nTubesPerPlane = None,
                  stPlaneMat=None, **kwds):
        self.material   = stPlaneMat
        self.nTubesPerPlane = nTubesPerPlane
        self.STPlaneBldr = self.get_builder('ST')


    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):


        sTube_lv   = self.STPlaneBldr.get_volume('volStrawTube_ST')
        straw_lv   = self.STPlaneBldr.get_volume('volStraw_ST')
        wire_lv    = self.STPlaneBldr.get_volume('volWire_ST')

        pS_in_Tube = geom.structure.Placement( 'placeS_in_Tube_'+self.name, volume = straw_lv )
        pW_in_Tube = geom.structure.Placement( 'placeW_in_Tube_'+self.name, volume = wire_lv )
        sTube_lv.placements.append( pS_in_Tube.name )
        sTube_lv.placements.append( pW_in_Tube.name )
        self.add_volume(sTube_lv)

        # Make the double-layer of straw tubes, used for both orientations
        #   note that it is not perfectly square in xy-- not quite as
        #   wide as the sTubes are long
        self.stPlaneDim = [ (self.nTubesPerPlane + 0.5)*self.sTube_outerDia, 
                            self.sTube_length, 
                            self.sTube_outerDia*( 1 + math.sin( math.radians(60) ) ) ]
        stPlaneBox = geom.shapes.Box( self.name,                 dx=0.5*self.stPlaneDim[0], 
                                      dy=0.5*self.stPlaneDim[1], dz=0.5*self.stPlaneDim[2])
        stPlane_lv = geom.structure.Volume('vol'+self.name, material=self.material, shape=stPlaneBox)
        self.add_volume(stPlane_lv)


        for i in range(self.nTubesPerPlane):

            #     <--- O O O O O O    ^      <--B_i+n    For each i, place ith A at (x,y,z) and
            #      +x   O O O O O O   | +z   <--A_i       place (i+n)th B at (x_next,y,-z),
            #                         |                   where n is number of tubes per plane

            xpos      = -0.5*self.stPlaneDim[0] + (i+0.5)*self.sTube_outerDia
            xpos_next =  xpos + 0.5*self.sTube_outerDia
            ypos      =  '0cm'
            zpos      = -0.5*self.stPlaneDim[2] + 0.5*self.sTube_outerDia


            # define positions, append placements
            st_in_p      = geom.structure.Position( 'Tube-'+str(i)+'_in_'+self.name, 
                                                    xpos,      ypos,  zpos)
            stnext_in_p  = geom.structure.Position( 'Tube-'+str(i+self.nTubesPerPlane)+'_in_'+self.name, 
                                                    xpos_next, ypos, -zpos)

            pst_in_p     = geom.structure.Placement( 'placeTube-'+str(i)+'_in_'+self.name,
                                                     volume = sTube_lv,
                                                     pos = st_in_p,
                                                     rot = "r90aboutX")
            pstnext_in_p = geom.structure.Placement( 'placeTube-'+str(i+self.nTubesPerPlane)+'_in_'+self.name,
                                                     volume = sTube_lv,
                                                     pos = stnext_in_p,
                                                     rot = "r90aboutX")


            stPlane_lv.placements.append( pst_in_p.name     )
            stPlane_lv.placements.append( pstnext_in_p.name )
