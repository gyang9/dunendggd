#!/usr/bin/env python
'''
Subbulder of StrawTubeBuilder
'''

import gegede.builder
from gegede import Quantity as Q
import math


class StrawTubeBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, actDimension=None, actMaterial=None,
                    actSTDimension = None, actSTMaterial=None,
                    actWireDimension=None, actWireMaterial=None, **kwds):
        self.actDimension, self.actMaterial = ( actDimension, actMaterial )
        self.actSTDimension, self.actSTMaterial = ( actSTDimension, actSTMaterial )
        self.actWireDimension, self.actWireMaterial = ( actWireDimension, actWireMaterial )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Make the straw tube shape and volume, and add straw into it
        # rmin=0, else material at 0 would be default of STPlane
        main_shape = geom.shapes.Tubs(self.name, rmin = self.actDimension["rmin"],
                                      rmax = self.actDimension["rmax"], dz = self.actDimension["dz"])
        main_lv   = geom.structure.Volume(self.name+"_lv", material=self.actMaterial, shape=main_shape)

        straw_shape = geom.shapes.Tubs(self.name+"_straw", rmin = self.actSTDimension["rmin"],
                                      rmax = self.actSTDimension["rmax"], dz = self.actSTDimension["dz"])
        straw_lv   = geom.structure.Volume(self.name+"_straw_lv", material=self.actSTMaterial, shape=straw_shape)

        wire_shape = geom.shapes.Tubs(self.name+"_wire", self.actWireDimension["rmin"],
                                      rmax = self.actSTDimension["rmax"], dz = self.actSTDimension["dz"])
        wire_lv    = geom.structure.Volume('volWire_'+self.name, material=self.actWireMaterial, shape=wire_shape)

        pS_in_Tube = geom.structure.Placement( 'placeS_in_Tube_'+self.name, volume = straw_lv )
        pW_in_Tube = geom.structure.Placement( 'placeW_in_Tube_'+self.name, volume = wire_lv )
        main_lv.placements.append( pS_in_Tube.name )
        main_lv.placements.append( pW_in_Tube.name )

        self.add_volume(main_lv)
