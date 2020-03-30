""" Module.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleBuilder(gegede.builder.Builder):
    """ Class to build Module geometry.

    """

    def configure(self,Bucket_Offset,InnerDetector_Offset,**kwargs):

        # Read dimensions form config file
        self.Bucket_Offset          = Bucket_Offset
        self.InnerDetector_Offset   = InnerDetector_Offset

        # Material definitons

        self.Material   = 'LAr'

        # Subbuilders
        self.Flange_builder         = self.get_builder('Flange')
        self.Bucket_builder         = self.get_builder('Bucket')
        self.Pillow_builder         = self.get_builder('Pillow')
        self.InnerDetector_builder  = self.get_builder('InnerDetector')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Flange_builder.halfDimension['dx'],
                                'dy':   self.Bucket_Offset+self.Bucket_builder.halfDimension['dy'],
                                'dz':   self.Flange_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build Flange
        pos = [Q('0cm'),self.halfDimension['dy']-self.Flange_builder.halfDimension['dy'],Q('0cm')]

        Flange_lv = self.Flange_builder.get_volume()

        Flange_pos = geom.structure.Position(self.Flange_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Flange_pla = geom.structure.Placement(self.Flange_builder.name+'_pla',
                                                volume=Flange_lv,
                                                pos=Flange_pos)

        main_lv.placements.append(Flange_pla.name)

        # Build Bucket
        pos = [Q('0cm'),self.halfDimension['dy']-self.Bucket_builder.halfDimension['dy']-2*self.Bucket_Offset,Q('0cm')]

        Bucket_lv = self.Bucket_builder.get_volume()

        Bucket_pos = geom.structure.Position(self.Bucket_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Bucket_pla = geom.structure.Placement(self.Bucket_builder.name+'_pla',
                                                volume=Bucket_lv,
                                                pos=Bucket_pos)

        main_lv.placements.append(Bucket_pla.name)

        # Build Pillow
        pos = [Q('0cm'),self.halfDimension['dy']-self.Pillow_builder.halfDimension['dy']-2*self.Flange_builder.halfDimension['dy'],Q('0cm')]

        Pillow_lv = self.Pillow_builder.get_volume()

        Pillow_pos = geom.structure.Position(self.Pillow_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Pillow_pla = geom.structure.Placement(self.Pillow_builder.name+'_pla',
                                                volume=Pillow_lv,
                                                pos=Pillow_pos)

        main_lv.placements.append(Pillow_pla.name)

        # Build Inner Detector
        pos = [Q('0cm'),self.halfDimension['dy']-self.InnerDetector_builder.halfDimension['dy']-2*self.InnerDetector_Offset,Q('0cm')]

        InnerDetector_lv = self.InnerDetector_builder.get_volume()

        InnerDetector_pos = geom.structure.Position(self.InnerDetector_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        InnerDetector_pla = geom.structure.Placement(self.InnerDetector_builder.name+'_pla',
                                                volume=InnerDetector_lv,
                                                pos=InnerDetector_pos)

        main_lv.placements.append(InnerDetector_pla.name)

