""" Bucket.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class BucketBuilder(gegede.builder.Builder):
    """ Class to build Bucket geometry.

    """

    def configure(self,G10Side_dimension,G10Bottom_dimension,LArVol1_dimension,LArVol2_dimension,LAr_Level_Bucket,**kwargs):

        # Read dimensions form config file
        self.G10Side_dx             = G10Side_dimension['dx']
        self.G10Side_dy             = G10Side_dimension['dy']
        self.G10Side_dz             = G10Side_dimension['dz']
        self.G10Side_dd             = G10Side_dimension['dd']

        self.G10Bottom_dx           = G10Bottom_dimension['dx']
        self.G10Bottom_dy           = G10Bottom_dimension['dy']
        self.G10Bottom_dz           = G10Bottom_dimension['dz']

        self.LArVol1_dx             = LArVol1_dimension['dx']
        self.LArVol1_dy             = LArVol1_dimension['dy']
        self.LArVol1_dz             = LArVol1_dimension['dz']

        self.LArVol2_dx             = LArVol2_dimension['dx']
        self.LArVol2_dy             = LArVol2_dimension['dy']
        self.LArVol2_dz             = LArVol2_dimension['dz']

        self.LAr_dy                 = LAr_Level_Bucket
        self.GAr_dy                 = self.G10Side_dy-self.LAr_dy

        # Material definitons
        self.G10_Material           = 'G10'
        self.LArPhase_Material      = 'LAr'
        self.GArPhase_Material      = 'GAr'

        self.Material               = 'GAr'

        self.Bucket_dx              = self.G10Side_dx
        self.Bucket_dy              = self.G10Side_dy
        self.Bucket_dz              = self.G10Side_dz

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Bucket_dx,
                                'dy':   self.Bucket_dy,
                                'dz':   self.Bucket_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('BucketBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct G10 Side Volume
        G10Side_shape = geom.shapes.Box('G10Side_shape',
                                        dx = self.G10Side_dx,
                                        dy = self.G10Side_dy,
                                        dz = self.G10Side_dz)

        G10Side_lv = geom.structure.Volume('volG10Side',
                                        material=self.G10_Material,
                                        shape=G10Side_shape)

        # Place G10 Side Volume inside Bucket volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.G10Side_dy,Q('0cm')]

        G10Side_pos = geom.structure.Position('G10Side_pos',
                                                pos[0],pos[1],pos[2])

        G10Side_pla = geom.structure.Placement('G10Side_pla',
                                                volume=G10Side_lv,
                                                pos=G10Side_pos)

        main_lv.placements.append(G10Side_pla.name)

        # Construct LAr Phase G10 Side Volume
        LArPhaseG10Side_shape = geom.shapes.Box('LArPhaseG10Side_shape',
                                        dx = self.G10Side_dx-self.G10Side_dd*2,
                                        dy = self.LAr_dy,
                                        dz = self.G10Side_dz-self.G10Side_dd*2)

        LArPhaseG10Side_lv = geom.structure.Volume('volLArPhaseG10Side',
                                        material=self.LArPhase_Material,
                                        shape=LArPhaseG10Side_shape)

        # Place LAr Phase G10 Side Volume inside Bucket volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.LAr_dy,Q('0cm')]

        LArPhaseG10Side_pos = geom.structure.Position('LArPhaseG10Side_pos',
                                                pos[0],pos[1],pos[2])

        LArPhaseG10Side_pla = geom.structure.Placement('LArPhaseG10Side_pla',
                                                volume=LArPhaseG10Side_lv,
                                                pos=LArPhaseG10Side_pos)

        main_lv.placements.append(LArPhaseG10Side_pla.name)

        # Construct GAr Phase G10 Side Volume
        GArPhaseG10Side_shape = geom.shapes.Box('GArPhaseG10Side_shape',
                                        dx = self.G10Side_dx-self.G10Side_dd*2,
                                        dy = self.GAr_dy,
                                        dz = self.G10Side_dz-self.G10Side_dd*2)

        GArPhaseG10Side_lv = geom.structure.Volume('volGArPhaseG10Side',
                                        material=self.GArPhase_Material,
                                        shape=GArPhaseG10Side_shape)

        # Place GAr Phase G10 Side Volume inside Bucket volume
        pos = [Q('0cm'),-self.halfDimension['dy']+2*self.LAr_dy+self.GAr_dy,Q('0cm')]

        GArPhaseG10Side_pos = geom.structure.Position('GArPhaseG10Side_pos',
                                                pos[0],pos[1],pos[2])

        GArPhaseG10Side_pla = geom.structure.Placement('GArPhaseG10Side_pla',
                                                volume=GArPhaseG10Side_lv,
                                                pos=GArPhaseG10Side_pos)

        main_lv.placements.append(GArPhaseG10Side_pla.name)

        # Construct G10 Bottom Volume
        G10Bottom_shape = geom.shapes.Box('G10Bottom_shape',
                                        dx = self.G10Bottom_dx,
                                        dy = self.G10Bottom_dy,
                                        dz = self.G10Bottom_dz)

        G10Bottom_lv = geom.structure.Volume('volG10Bottom',
                                        material=self.G10_Material,
                                        shape=G10Bottom_shape)

        # Place G10 Bottom Volume inside Bucket volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.G10Bottom_dy,Q('0cm')]

        G10Bottom_pos = geom.structure.Position('G10Bottom_pos',
                                                pos[0],pos[1],pos[2])

        G10Bottom_pla = geom.structure.Placement('G10Bottom_pla',
                                                volume=G10Bottom_lv,
                                                pos=G10Bottom_pos)

        main_lv.placements.append(G10Bottom_pla.name)

        # Construct LAr Volume 1
        LArVol1_shape = geom.shapes.Box('LArVol1_shape',
                                        dx = self.LArVol1_dx,
                                        dy = self.LArVol1_dy+self.LArVol2_dy,
                                        dz = self.LArVol1_dz)

        LArVol1_lv = geom.structure.Volume('volLArVol1',
                                        material=self.LArPhase_Material,
                                        shape=LArVol1_shape)

        # Place LAr Volume 1 inside Bucket volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.LArVol1_dy+self.LArVol2_dy,Q('0cm')]

        LArVol1_pos = geom.structure.Position('LArVol1_pos',
                                                pos[0],pos[1],pos[2])

        LArVol1_pla = geom.structure.Placement('LArVol1_pla',
                                                volume=LArVol1_lv,
                                                pos=LArVol1_pos)

        main_lv.placements.append(LArVol1_pla.name)

        # Construct LAr Volume 2
        LArVol2_shape = geom.shapes.Box('LArVol2_shape',
                                        dx = self.LArVol2_dx,
                                        dy = self.LArVol2_dy,
                                        dz = self.LArVol2_dz)

        LArVol2_lv = geom.structure.Volume('volLArVol2',
                                        material=self.LArPhase_Material,
                                        shape=LArVol2_shape)

        # Place LAr Volume 2 inside Bucket volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.LArVol2_dy,Q('0cm')]

        LArVol2_pos = geom.structure.Position('LArVol2_pos',
                                                pos[0],pos[1],pos[2])

        LArVol2_pla = geom.structure.Placement('LArVol2_pla',
                                                volume=LArVol2_lv,
                                                pos=LArVol2_pos)

        main_lv.placements.append(LArVol2_pla.name)

