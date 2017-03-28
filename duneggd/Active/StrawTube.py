#!/usr/bin/env python
import gegede.builder
from gegede import Quantity as Q
import math

class StrawTubeBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None,
                    halfSTDimension = None, STMaterial=None,
                    halfWireDimension=None, WireMaterial=None, **kwds):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.halfSTDimension, self.STMaterial = ( halfSTDimension, STMaterial )
        self.halfWireDimension, self.WireMaterial = ( halfWireDimension, WireMaterial )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Make the straw tube shape and volume, and add straw into it
        # rmin=0, else material at 0 would be default of STPlane
        main_shape = geom.shapes.Tubs(self.name, rmin = self.halfDimension["rmin"],
                                      rmax = self.halfDimension["rmax"], dz = self.halfDimension["dz"])
        main_lv   = geom.structure.Volume(self.name+"_lv", material=self.Material, shape=main_shape)

        straw_shape = geom.shapes.Tubs(self.name+"_straw", rmin = self.halfSTDimension["rmin"],
                                      rmax = self.halfSTDimension["rmax"], dz = self.halfSTDimension["dz"])
        straw_lv   = geom.structure.Volume(self.name+"_straw_lv", material=self.STMaterial, shape=straw_shape)

        wire_shape = geom.shapes.Tubs(self.name+"_wire", self.halfWireDimension["rmin"],
                                      rmax = self.halfSTDimension["rmax"], dz = self.halfSTDimension["dz"])
        wire_lv    = geom.structure.Volume('volWire_'+self.name, material=self.WireMaterial, shape=wire_shape)

        pS_in_Tube = geom.structure.Placement( 'placeS_in_Tube_'+self.name, volume = straw_lv )
        pW_in_Tube = geom.structure.Placement( 'placeW_in_Tube_'+self.name, volume = wire_lv )
        main_lv.placements.append( pS_in_Tube.name )
        main_lv.placements.append( pW_in_Tube.name )

        self.add_volume(main_lv)
