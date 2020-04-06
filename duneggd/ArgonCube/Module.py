""" Module.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleBuilder(gegede.builder.Builder):
    """ Class to build Module geometry.

    """

    def configure(self,**kwargs):

        # Read dimensions form config file

        # Material definitons

        self.Material   = 'GAr'

        # Subbuilders
        self.Flange_builder         = self.get_builder('Flange')
        self.Bucket_builder         = self.get_builder('Bucket')
        self.Feedthrough_builder    = self.get_builder('Feedthrough')
        self.Pillow_builder         = self.Flange_builder.get_builder('Pillow')
        self.HVFeedThrough_builder  = self.get_builder('HVFeedThrough')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Flange_builder.halfDimension['dx'],
                                'dy':   self.Flange_builder.halfDimension['dy']+self.Bucket_builder.halfDimension['dy'],
                                'dz':   self.Flange_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build Flange
        pos = [Q('0cm'),self.Bucket_builder.halfDimension['dy'],Q('0cm')]

        Flange_lv = self.Flange_builder.get_volume()

        Flange_pos = geom.structure.Position(self.Flange_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Flange_pla = geom.structure.Placement(self.Flange_builder.name+'_pla',
                                                volume=Flange_lv,
                                                pos=Flange_pos)

        main_lv.placements.append(Flange_pla.name)

        # Build Bucket
        pos = [Q('0cm'),-self.Flange_builder.halfDimension['dy'],Q('0cm')]

        Bucket_lv = self.Bucket_builder.get_volume()

        Bucket_pos = geom.structure.Position(self.Bucket_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Bucket_pla = geom.structure.Placement(self.Bucket_builder.name+'_pla',
                                                volume=Bucket_lv,
                                                pos=Bucket_pos)

        main_lv.placements.append(Bucket_pla.name)

        # Build Feedthrough
        pos = [Q('0cm'),self.halfDimension['dy']+self.Feedthrough_builder.halfDimension['dy']-2*self.Pillow_builder.PillowSide_dy-2*self.Flange_builder.halfDimension['dy'],Q('0cm')]

        Feedthrough_lv = self.Feedthrough_builder.get_volume()

        Feedthrough_pos = geom.structure.Position(self.Feedthrough_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Feedthrough_pla = geom.structure.Placement(self.Feedthrough_builder.name+'_pla',
                                                volume=Feedthrough_lv,
                                                pos=Feedthrough_pos)

        main_lv.placements.append(Feedthrough_pla.name)

        # Build HVFeedThrough
        pos = [Q('0cm'),self.halfDimension['dy'],Q('0cm')]

        rot_x = Q('90.0deg')

        HVFeedThrough_lv = self.HVFeedThrough_builder.get_volume()

        HVFeedThrough_pos = geom.structure.Position(self.HVFeedThrough_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        HVFeedThrough_rot = geom.structure.Rotation(self.HVFeedThrough_builder.name+'_rot',
                                                rot_x)

        HVFeedThrough_pla = geom.structure.Placement(self.HVFeedThrough_builder.name+'_pla',
                                                volume=HVFeedThrough_lv,
                                                pos=HVFeedThrough_pos,
                                                rot=HVFeedThrough_rot)

        main_lv.placements.append(HVFeedThrough_pla.name)

