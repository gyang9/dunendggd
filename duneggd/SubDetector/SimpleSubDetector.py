#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class SimpleSubDetectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, NElements=None,  InsideGap=None,
                    BeginGap=None, TranspV=None, Rotation=None, Sensitive=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.NElements, self.InsideGap = ( NElements, InsideGap )
        self.BeginGap, self.TranspV = ( BeginGap, TranspV )
        self.Rotation, self.Sensitive = ( Rotation, Sensitive )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        if isinstance(self.Sensitive,str):
            main_lv.params.append(("SensDet",self.Sensitive))
        self.add_volume( main_lv )

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.Rotation[0]),
                                                str(self.Rotation[1]),  str(self.Rotation[2]) )

        # get sub-builders and its logic volume
        sb = self.get_builder()
        sb_lv = sb.get_volume()

        # initial position, based on the dimension projected on transportation vector
        pos = ltools.getInitialPos( self, main_hDim )

        for elem in range(self.NElements):
            sb_dim = ltools.getShapeDimensions( sb_lv, geom )
            step = [ t*d for t,d in zip(self.TranspV, sb_dim) ]
            pos = [ p+s for p,s in zip(pos,step) ]
            sb_pos = geom.structure.Position(self.name+sb_lv.name+str(elem)+'_pos',
                                                        pos[0], pos[1], pos[2])
            sb_pla = geom.structure.Placement(self.name+sb_lv.name+str(elem)+'_pla',
                                                        volume=sb_lv, pos=sb_pos, rot =rotation)
            main_lv.placements.append(sb_pla.name)
            pos = [p+s+t*self.InsideGap for p,s,t in zip(pos,step,self.TranspV)]
