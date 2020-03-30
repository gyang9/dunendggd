""" Module.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleBuilder(gegede.builder.Builder):
    """ Class to build Module geometry.

    """

    def configure(self,Module_dimension,Bucket_Offset,InnerDetector_Offset,**kwargs):

        # Read dimensions form config file
        self.Module_dx          = Module_dimension['dx']
        self.Module_dy          = Module_dimension['dy']
        self.Module_dz          = Module_dimension['dz']

        self.Bucket_Offset          = Bucket_Offset
        self.InnerDetector_Offset   = InnerDetector_Offset

        # Material definitons

        self.Material           = 'Air'

        # Subbuilders
        self.Bucket_builder         = self.get_builder('Bucket')
        self.ModuleTop_builder      = self.get_builder('ModuleTop')
        self.InnerDetector_builder  = self.get_builder('InnerDetector')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.ModuleTop_builder.halfDimension['dx'],
                                'dy':   self.InnerDetector_Offset+self.Bucket_builder.halfDimension['dy'],
                                'dz':   self.ModuleTop_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build Bucket
        pos = [Q('0cm'),self.halfDimension['dy']-self.Bucket_builder.halfDimension['dy']-self.Bucket_Offset*2,Q('0cm')]

        Bucket_lv = self.Bucket_builder.get_volume()

        Bucket_pos = geom.structure.Position(self.Bucket_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Bucket_pla = geom.structure.Placement(self.Bucket_builder.name+'_pla',
                                                volume=Bucket_lv,
                                                pos=Bucket_pos)

        main_lv.placements.append(Bucket_pla.name)


        # Build Module Top
        pos = [Q('0cm'),self.halfDimension['dy']-self.ModuleTop_builder.halfDimension['dy'],Q('0cm')]

        ModuleTop_lv = self.ModuleTop_builder.get_volume()

        ModuleTop_pos = geom.structure.Position(self.ModuleTop_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        ModuleTop_pla = geom.structure.Placement(self.ModuleTop_builder.name+'_pla',
                                                volume=ModuleTop_lv,
                                                pos=ModuleTop_pos)

        main_lv.placements.append(ModuleTop_pla.name)

        # Build Inner Detector
        pos = [Q('0cm'),self.halfDimension['dy']-self.InnerDetector_builder.halfDimension['dy']-self.InnerDetector_Offset*2,Q('0cm')]

        InnerDetector_lv = self.InnerDetector_builder.get_volume()

        InnerDetector_pos = geom.structure.Position(self.InnerDetector_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        InnerDetector_pla = geom.structure.Placement(self.InnerDetector_builder.name+'_pla',
                                                volume=InnerDetector_lv,
                                                pos=InnerDetector_pos)

        main_lv.placements.append(InnerDetector_pla.name)

