#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class LArStructureBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, InsideGap=None,
                    BField=None, EField=None, Sensitive=None,
                    SubBPos=None, Boolean=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.InsideGap = InsideGap
        self.BField, self.EField = ( BField, EField )
        self.Sensitive = Sensitive

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # PARTICULAR GEOMETRY, IT IS NO GENERAL, NO EVERYONE CAN USE
        #(xyz- = xyzn, xyz+ = xyzp)
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        sb_boolean_shape = geom.store.shapes.get(main_lv.shape)
        builders = self.get_builders()

        #XY (-Z)
        sb_xyzn = builders[0]
        sb_xyzn_lv = sb_xyzn.get_volume()
        sb_xyzn_shape = geom.store.shapes.get(sb_xyzn_lv.shape)
        sb_pos = geom.structure.Position(self.name+'_pos_xyzn', Q('0cm'), Q('0cm'),
                                            -main_hDim[2]+sb_xyzn.halfDimension['dz'] )
        sb_boolean_shape = geom.shapes.Boolean( self.name+'_xyzn',
                                                type='intersection', first=sb_boolean_shape,
                                                second=sb_xyzn_shape, pos=sb_pos)

        #XY (+Z)
        sb_xyzp = builders[1]
        sb_xyzp_lv = sb_xyzp.get_volume()
        sb_xyzp_shape = geom.store.shapes.get(sb_xyzp_lv.shape)
        sb_pos = geom.structure.Position(self.name+'_pos_xyzp', Q('0cm'), Q('0cm'),
                                            main_hDim[2]-sb_xyzp.halfDimension['dz'] )
        sb_boolean_shape = geom.shapes.Boolean( self.name+'_xyzp',
                                                type='union', first=sb_boolean_shape,
                                                second=sb_xyzp_shape, pos=sb_pos)

        #YZ (-X)
        sb_yzxn = builders[2]
        sb_yzxn_lv = sb_yzxn.get_volume()
        sb_yzxn_shape = geom.store.shapes.get(sb_yzxn_lv.shape)
        sb_pos = geom.structure.Position(self.name+'_pos_yzxn', -main_hDim[0]+sb_yzxn.halfDimension['dx'],
                                        Q('0cm'), Q('0cm') )
        sb_boolean_shape = geom.shapes.Boolean( self.name+'_yzxn',
                                                type='union', first=sb_boolean_shape,
                                                second=sb_yzxn_shape, pos=sb_pos)

        #YZ (+X)
        sb_yzxp = builders[3]
        sb_yzxp_lv = sb_yzxp.get_volume()
        sb_yzxp_shape = geom.store.shapes.get(sb_yzxp_lv.shape)
        sb_pos = geom.structure.Position(self.name+'_pos_yzxp', +main_hDim[0]-sb_yzxp.halfDimension['dx'],
                                        Q('0cm'), Q('0cm') )
        sb_boolean_shape = geom.shapes.Boolean( self.name+'_yzxp',
                                                type='union', first=sb_boolean_shape,
                                                second=sb_yzxp_shape, pos=sb_pos)
        #XZ (-Y)
        sb_xzyn = builders[4]
        sb_xzyn_lv = sb_xzyn.get_volume()
        sb_xzyn_shape = geom.store.shapes.get(sb_xzyn_lv.shape)
        sb_pos = geom.structure.Position(self.name+'_pos_xzyn', Q('0cm'),
                                        -main_hDim[1]+sb_xzyn.halfDimension['dy']+Q('20cm'), Q('0cm') )
        sb_boolean_shape = geom.shapes.Boolean( self.name+'_xzyn',
                                                type='union', first=sb_boolean_shape,
                                                second=sb_xzyn_shape, pos=sb_pos)

        sb_boolean_lv = geom.structure.Volume('vol'+sb_boolean_shape.name, material=self.Material,
                                                shape=sb_boolean_shape)

        if isinstance(self.Sensitive,str):
            sb_boolean_lv.params.append(("SensDet",self.Sensitive))
        if isinstance(self.BField,str):
            sb_boolean_lv.params.append(("BField",self.BField))
        if isinstance(self.EField,str):
            sb_boolean_lv.params.append(("EField",self.EField))

        self.add_volume( sb_boolean_lv )
