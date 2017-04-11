#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class PrimaryBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None, InsideGap=None,
                        TranspV=None, Rotation=None, **kwds):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.InsideGap = InsideGap
        self.TranspV, self.Rotation = ( TranspV, Rotation )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume( main_lv )

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.Rotation[0]),
                                                str(self.Rotation[1]),  str(self.Rotation[2]) )

        # lower edge, using builder and sub-builder dimension projected on transportation vector
        low_edge = [-t*d for t,d in zip(self.TranspV,main_hDim)]

        for i,sb in enumerate(self.get_builders()):
            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get(sb_lv.shape)
            sb_dim = [sb_shape.dx,sb_shape.dy,sb_shape.dz]
            # lower edge, using builder and sub-builder dimension projected on transportation vector
            low_edge = [le+t*(sbd+self.InsideGap[i]) for le,t,sbd in zip(low_edge, self.TranspV,sb_dim)]
            # defining position, placement, and finally insert into main logic volume.
            sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos',
                                                low_edge[0], low_edge[1], low_edge[2])
            sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla',
                                                volume=sb_lv, pos=sb_pos, rot =rotation)
            main_lv.placements.append(sb_pla.name)
            low_edge = [le+t*sbd for le,t,sbd in zip(low_edge, self.TranspV,sb_dim)]
