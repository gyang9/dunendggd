""" Module.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleBuilder(gegede.builder.Builder):
    """ Class to build Module geometry.

    """

    def configure(self,Module_dimension,Bucket_offset,InnerDet_offset,**kwargs):

        # Read dimensions form config file
        self.Module_dx          = Module_dimension['dx']
        self.Module_dy          = Module_dimension['dy']
        self.Module_dz          = Module_dimension['dz']

        self.Bucket_offset      = Bucket_offset
        self.InnerDet_offset    = InnerDet_offset

        # Material definitons

        self.Material           = 'Air'

        # Subbuilders
        self.bucket_builder     = self.get_builder('BucketAss')
        self.moduleTop_builder  = self.get_builder('ModuleTop')
        self.innerDet_builder   = self.get_builder('InnerDetector')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.moduleTop_builder.halfDimension['dx'],
                                'dy':   self.InnerDet_offset+self.bucket_builder.halfDimension['dy'],
                                'dz':   self.moduleTop_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build Bucket
        pos = [Q('0cm'),self.halfDimension['dy']-self.bucket_builder.halfDimension['dy']-self.Bucket_offset*2,Q('0cm')]

        bucket_lv = self.bucket_builder.get_volume()

        bucket_pos = geom.structure.Position(self.bucket_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        bucket_pla = geom.structure.Placement(self.bucket_builder.name+'_pla',
                                                volume=bucket_lv,
                                                pos=bucket_pos)

        main_lv.placements.append(bucket_pla.name)


        # Build Module Top
        pos = [Q('0cm'),self.halfDimension['dy']-self.moduleTop_builder.halfDimension['dy'],Q('0cm')]

        moduleTop_lv = self.moduleTop_builder.get_volume()

        moduleTop_pos = geom.structure.Position(self.moduleTop_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        moduleTop_pla = geom.structure.Placement(self.moduleTop_builder.name+'_pla',
                                                volume=moduleTop_lv,
                                                pos=moduleTop_pos)

        main_lv.placements.append(moduleTop_pla.name)

        # Build Inner Detector
        pos = [Q('0cm'),self.halfDimension['dy']-self.innerDet_builder.halfDimension['dy']-self.InnerDet_offset*2,Q('0cm')]

        innerDet_lv = self.innerDet_builder.get_volume()

        innerDet_pos = geom.structure.Position(self.innerDet_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        innerDet_pla = geom.structure.Placement(self.innerDet_builder.name+'_pla',
                                                volume=innerDet_lv,
                                                pos=innerDet_pos)

        main_lv.placements.append(innerDet_pla.name)

