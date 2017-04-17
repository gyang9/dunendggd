#!/usr/bin/env python
import gegede.builder
from gegede import Quantity as Q

class StrawTubeBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None,
                    halfSTDimension = None, STMaterial=None,
                    halfWireDimension=None, WireMaterial=None, **kwds):
        """
        :param halfDimension: halfDimension for the whole Straw Tube.
        :type halfDimension: dictionary
        :param Material: Material for the whole Straw Tube.
        :type Material: defined on World.py.
        :param halfSTDimension: halfSTDimension for the Straw Tube case.
        :type halfSTDimension: dictionary
        :param STMaterial: Material for the Straw Tube case.
        :type STMaterial: defined on World.py.
        :param halfWireDimension: halfSTDimension for the wire.
        :type halfWireDimension: dictionary
        :param WireMaterial: Material for the wire.
        :type WireMaterial: defined on World.py.
        :returns: None
        """
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.halfSTDimension, self.STMaterial = ( halfSTDimension, STMaterial )
        self.halfWireDimension, self.WireMaterial = ( halfWireDimension, WireMaterial )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        """
        Construct the geometry for Straw Tube Bar.
        :returns: None
        """
        wire_shape = geom.shapes.Tubs(self.name+"_wire", self.halfWireDimension["rmin"],
                                              rmax = self.halfSTDimension["rmax"], dz = self.halfSTDimension["dz"])
        wire_lv    = geom.structure.Volume(self.name+"_wire_lv", material=self.WireMaterial, shape=wire_shape)
        #self.add_volume(wire_lv)

        straw_shape = geom.shapes.Tubs(self.name+"_straw", rmin = self.halfSTDimension["rmin"],
                                      rmax = self.halfSTDimension["rmax"], dz = self.halfSTDimension["dz"])
        straw_lv   = geom.structure.Volume(self.name+"_straw_lv", material=self.STMaterial, shape=straw_shape)
        #self.add_volume(straw_lv)

        main_shape = geom.shapes.Tubs(self.name, rmin = self.halfDimension["rmin"],
                                      rmax = self.halfDimension["rmax"], dz = self.halfDimension["dz"])
        main_lv   = geom.structure.Volume(self.name+"_lv", material=self.Material, shape=main_shape)
        self.add_volume(main_lv)

        pS_in_Tube = geom.structure.Placement( 'placeS_in_Tube_'+self.name, volume = straw_lv )
        pW_in_Tube = geom.structure.Placement( 'placeW_in_Tube_'+self.name, volume = wire_lv )
        main_lv.placements.append( pS_in_Tube.name )
        main_lv.placements.append( pW_in_Tube.name )
