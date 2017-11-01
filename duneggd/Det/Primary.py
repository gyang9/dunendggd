#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class PrimaryBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None, BeginGap=None,
                    InsideGap=None,  AuxParams=None, **kwds):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.BeginGap, self.InsideGap = ( BeginGap, InsideGap )
        self.AuxParams = AuxParams

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")

        if self.AuxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )


        TranspV = [0,0,1]
        begingap = ltools.getBeginGap( self )

        # initial position, based on the dimension projected on transportation vector
        pos = [Q('0m'),Q('0m'),-main_hDim[2]+begingap]

        for i,sb in enumerate(self.get_builders()):
            sb_lv = sb.get_volume()
            sb_dim = ltools.getShapeDimensions( sb_lv, geom )
            step = [Q('0cm'),Q('0cm'),Q('0cm')]
            #assert ( sb_dim != None ), " fail"
            if sb_dim != None:
                step[2] = sb_dim[2]
            else:
                assert( sb.halfDimension != None ), " No volumen defined on %s " % sb
                step[2] = sb.halfDimension['dz']
            pos[2] = pos[2] + step[2] + self.InsideGap[i]
            # defining position, placement, and finally insert into main logic volume.
            sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos_'+str(i),
                                                pos[0], pos[1], pos[2])
            sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla_'+str(i),
                                                volume=sb_lv, pos=sb_pos )
            main_lv.placements.append(sb_pla.name)
            pos[2] = pos[2] + step[2]
