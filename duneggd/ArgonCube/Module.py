""" Module.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleBuilder(gegede.builder.Builder):
    """ Class to build Module geometry.

    """

    def configure(self,Backplate_Offset,Pillow_Offset,InnerDetector_Offset,**kwargs):

        # Read dimensions form config file
        self.Backplate_Offset       = Backplate_Offset
        self.Pillow_Offset          = Pillow_Offset
        self.InnerDetector_Offset   = InnerDetector_Offset

        # Material definitons

        self.Material   = 'Air'

        # Subbuilders
        self.Bucket_builder         = self.get_builder('Bucket')
        self.Backplate_builder      = self.get_builder('Backplate')
        self.InnerDetector_builder  = self.get_builder('InnerDetector')
        self.Feedthrough_builder    = self.get_builder('Feedthrough')
        self.TPiece_builder         = self.get_builder('TPiece')
        self.HVFeedThrough_builder  = self.get_builder('HVFeedThrough')
        self.Flange_builder         = self.Feedthrough_builder.get_builder('Flange')
        self.Pillow_builder         = self.Feedthrough_builder.get_builder('Pillow')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Flange_builder.halfDimension['dx'],
                                'dy':   self.InnerDetector_Offset+self.InnerDetector_builder.halfDimension['dy']+self.HVFeedThrough_builder.halfDimension['dz'],
                                'dz':   self.Flange_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build Bucket
        pos = [Q('0cm'),-self.halfDimension['dy']+self.Bucket_builder.halfDimension['dy'],Q('0cm')]

        Bucket_lv = self.Bucket_builder.get_volume()

        Bucket_pos = geom.structure.Position(self.Bucket_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Bucket_pla = geom.structure.Placement(self.Bucket_builder.name+'_pla',
                                                volume=Bucket_lv,
                                                pos=Bucket_pos)

        main_lv.placements.append(Bucket_pla.name)

        # Build Backplate L
        pos = [-self.InnerDetector_builder.halfDimension['dx']-self.Backplate_builder.halfDimension['dx'],-self.halfDimension['dy']+self.Backplate_builder.halfDimension['dy']+2*self.Backplate_Offset,Q('0cm')]

        Backplate_lv = self.Backplate_builder.get_volume()

        Backplate_pos = geom.structure.Position(self.Backplate_builder.name+'_pos_L',
                                                pos[0],pos[1],pos[2])

        Backplate_pla = geom.structure.Placement(self.Backplate_builder.name+'_pla_L',
                                                volume=Backplate_lv,
                                                pos=Backplate_pos)

        main_lv.placements.append(Backplate_pla.name)

        # Build Backplate R
        pos = [self.InnerDetector_builder.halfDimension['dx']+self.Backplate_builder.halfDimension['dx'],-self.halfDimension['dy']+self.Backplate_builder.halfDimension['dy']+2*self.Backplate_Offset,Q('0cm')]

        Backplate_lv = self.Backplate_builder.get_volume()

        Backplate_pos = geom.structure.Position(self.Backplate_builder.name+'_pos_R',
                                                pos[0],pos[1],pos[2])

        Backplate_pla = geom.structure.Placement(self.Backplate_builder.name+'_pla_R',
                                                volume=Backplate_lv,
                                                pos=Backplate_pos)

        main_lv.placements.append(Backplate_pla.name)

        # Build Pillow
        pos = [Q('0cm'),-self.halfDimension['dy']+self.Pillow_builder.halfDimension['dy']+2*self.Pillow_Offset,Q('0cm')]

        Pillow_lv = self.Pillow_builder.get_volume()

        Pillow_pos = geom.structure.Position(self.Pillow_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Pillow_pla = geom.structure.Placement(self.Pillow_builder.name+'_pla',
                                                volume=Pillow_lv,
                                                pos=Pillow_pos)

        main_lv.placements.append(Pillow_pla.name)

        # Build Flange
        pos = [Q('0cm'),-self.halfDimension['dy']+2*self.Pillow_Offset+2*self.Pillow_builder.halfDimension['dy']+self.Flange_builder.halfDimension['dy'],Q('0cm')]

        Flange_lv = self.Flange_builder.get_volume()

        Flange_pos = geom.structure.Position(self.Flange_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Flange_pla = geom.structure.Placement(self.Flange_builder.name+'_pla',
                                                volume=Flange_lv,
                                                pos=Flange_pos)

        main_lv.placements.append(Flange_pla.name)

        # Build Inner Detector
        pos = [Q('0cm'),-self.halfDimension['dy']+self.InnerDetector_builder.halfDimension['dy']+2*self.InnerDetector_Offset,Q('0cm')]

        InnerDetector_lv = self.InnerDetector_builder.get_volume()

        InnerDetector_pos = geom.structure.Position(self.InnerDetector_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        InnerDetector_pla = geom.structure.Placement(self.InnerDetector_builder.name+'_pla',
                                                volume=InnerDetector_lv,
                                                pos=InnerDetector_pos)

        main_lv.placements.append(InnerDetector_pla.name)

        # Build Feedthrough
        pos = [Q('0cm'),-self.halfDimension['dy']+2*self.Pillow_Offset+2*self.Pillow_builder.halfDimension['dy']+self.Feedthrough_builder.halfDimension['dy']-2*self.Pillow_builder.PillowSide_dy,Q('0cm')]

        Feedthrough_lv = self.Feedthrough_builder.get_volume()

        Feedthrough_pos = geom.structure.Position(self.Feedthrough_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Feedthrough_pla = geom.structure.Placement(self.Feedthrough_builder.name+'_pla',
                                                volume=Feedthrough_lv,
                                                pos=Feedthrough_pos)

        main_lv.placements.append(Feedthrough_pla.name)

        # Build TPieces
        pos = [2*self.Feedthrough_builder.TubeSide_Offset,-self.halfDimension['dy']+2*self.Pillow_Offset+2*self.Pillow_builder.halfDimension['dy']-2*self.Pillow_builder.PillowSide_dy+2*self.Feedthrough_builder.TubeSide_dz+self.TPiece_builder.halfDimension['dy'],2*self.TPiece_builder.TPiece_dz_h-self.TPiece_builder.halfDimension['dz']]

        TPiece_lv = self.TPiece_builder.get_volume()

        TPiece_pos = geom.structure.Position(self.TPiece_builder.name+'_pos_A',
                                                pos[0],pos[1],pos[2])

        TPiece_pla = geom.structure.Placement(self.TPiece_builder.name+'_pla_A',
                                                volume=TPiece_lv,
                                                pos=TPiece_pos)

        main_lv.placements.append(TPiece_pla.name)

        pos = [-2*self.Feedthrough_builder.TubeSide_Offset,-self.halfDimension['dy']+2*self.Pillow_Offset+2*self.Pillow_builder.halfDimension['dy']-2*self.Pillow_builder.PillowSide_dy+2*self.Feedthrough_builder.TubeSide_dz+self.TPiece_builder.halfDimension['dy'],-2*self.TPiece_builder.TPiece_dz_h+self.TPiece_builder.halfDimension['dz']]

        rot = [Q('180.0deg'),Q('0.0deg'),Q('0.0deg')]

        TPiece_lv = self.TPiece_builder.get_volume()

        TPiece_pos = geom.structure.Position(self.TPiece_builder.name+'_pos_B',
                                                pos[0],pos[1],pos[2])

        TPiece_rot = geom.structure.Rotation(self.TPiece_builder.name+'_rot_B',
                                                rot[0],rot[1],rot[2])

        TPiece_pla = geom.structure.Placement(self.TPiece_builder.name+'_pla_B',
                                                volume=TPiece_lv,
                                                pos=TPiece_pos,
                                                rot=TPiece_rot)

        main_lv.placements.append(TPiece_pla.name)

        # Build HVFeedThrough
        pos = [Q('0cm'),-self.halfDimension['dy']+self.HVFeedThrough_builder.halfDimension['dz']+2*self.InnerDetector_Offset+2*self.InnerDetector_builder.halfDimension['dy'],Q('0cm')]

        rot = [Q('90.0deg'),Q('0.0deg'),Q('0.0deg')]

        HVFeedThrough_lv = self.HVFeedThrough_builder.get_volume()

        HVFeedThrough_pos = geom.structure.Position(self.HVFeedThrough_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        HVFeedThrough_rot = geom.structure.Rotation(self.HVFeedThrough_builder.name+'_rot',
                                                rot[0],rot[1],rot[2])

        HVFeedThrough_pla = geom.structure.Placement(self.HVFeedThrough_builder.name+'_pla',
                                                volume=HVFeedThrough_lv,
                                                pos=HVFeedThrough_pos,
                                                rot=HVFeedThrough_rot)

        main_lv.placements.append(HVFeedThrough_pla.name)

