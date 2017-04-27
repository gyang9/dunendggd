#!/usr/bin/env python
import gegede.builder
from gegede import Quantity as Q

class StrawTubeBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None,
                    halfSTDimension = None, STMaterial=None,
                    halfWireDimension=None, WireMaterial=None, Sensitive=None, **kwds):
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
        self.Sensitive = Sensitive

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        """
        Construct the geometry for Straw Tube Bar.
        :returns: None
        """

        main_shape = geom.shapes.Tubs(self.name, rmin = self.halfDimension["rmin"],
                                      rmax = self.halfDimension["rmax"], dz = self.halfDimension["dz"])
        main_lv   = geom.structure.Volume(self.name+"_lv", material=self.Material, shape=main_shape)
        if isinstance(self.Sensitive,str):
            main_lv.params.append(("SensDet",self.Sensitive))
        self.add_volume(main_lv)

        straw_shape = geom.shapes.Tubs(self.name+"_straw", rmin = self.halfSTDimension["rmin"],
                                      rmax = self.halfSTDimension["rmax"], dz = self.halfSTDimension["dz"])
        straw_lv   = geom.structure.Volume(self.name+"_straw_lv", material=self.STMaterial, shape=straw_shape)

        wire_shape = geom.shapes.Tubs(self.name+"_wire", self.halfWireDimension["rmin"],
                                              rmax = self.halfWireDimension["rmax"], dz = self.halfWireDimension["dz"])
        wire_lv    = geom.structure.Volume(self.name+"_wire_lv", material=self.WireMaterial, shape=wire_shape)

        straw_pla = geom.structure.Placement( self.name+"_straw_pla", volume = straw_lv )
        wire_pla = geom.structure.Placement( self.name+"_wire_pla", volume = wire_lv )
        main_lv.placements.append( straw_pla.name )
        main_lv.placements.append( wire_pla.name )
