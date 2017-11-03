#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class TPCPixelBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None, halfCopperDimension=None,
                    Sensitive=None, **kwds):
        """
        :param halfDimension: halfDimension for the whole Straw Tube.
        :type halfDimension: dictionary
        :param Material: Material for the whole Straw Tube.
        :type Material: defined on World.py.
        :returns: None
        """
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.halfCopperDimension, self.Sensitive = halfCopperDimension, Sensitive

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        """
        Construct the geometry for Straw Tube Bar.
        :returns: None
        """
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        if isinstance(self.Sensitive,str):
            main_lv.params.append(("SensDet",self.Sensitive))
        self.add_volume(main_lv)

        copper_shape = geom.shapes.Tubs(self.name+"_copper", rmin = self.halfCopperDimension["rmin"],
                                        rmax = self.halfCopperDimension["rmax"],
                                        dz   = self.halfCopperDimension["dz"])
        copper_lv    = geom.structure.Volume(self.name+"_copper_lv", material="Copper", shape=copper_shape)

        copper_pla = geom.structure.Placement( self.name+"_copper_pla", volume = copper_lv )
        main_lv.placements.append( copper_pla.name )
