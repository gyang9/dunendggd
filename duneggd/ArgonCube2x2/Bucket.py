""" Bucket.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class BucketBuilder(gegede.builder.Builder):
    """ Class to build Bucket geometry.

    """

    def configure(self,Bucket_dimension,G10Bottom_dimension,LArVol1_dimension,LArVol2_dimension,LAr_Level_Bucket,**kwargs):

        # Read dimensions form config file
        self.Bucket_dx          = Bucket_dimension['dx']
        self.Bucket_dy          = Bucket_dimension['dy']
        self.Bucket_dz          = Bucket_dimension['dz']
        self.Bucket_dd          = Bucket_dimension['dd']

        self.G10Bottom_dx       = G10Bottom_dimension['dx']
        self.G10Bottom_dy       = G10Bottom_dimension['dy']
        self.G10Bottom_dz       = G10Bottom_dimension['dz']

        self.LArVol1_dx         = LArVol1_dimension['dx']
        self.LArVol1_dy         = LArVol1_dimension['dy']
        self.LArVol1_dz         = LArVol1_dimension['dz']

        self.LArVol2_dx         = LArVol2_dimension['dx']
        self.LArVol2_dy         = LArVol2_dimension['dy']
        self.LArVol2_dz         = LArVol2_dimension['dz']

        self.LAr_dy             = LAr_Level_Bucket
        self.GAr_dy             = self.Bucket_dy-self.LAr_dy

        # Material definitons
        self.Bucket_Material    = 'G10'
        self.LArPhase_Material  = 'LAr'
        self.GArPhase_Material  = 'GAr'

        self.Material           = 'G10'

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

        # Construct LAr Phase Bucket Volume
        LArPhaseBucket_shape = geom.shapes.Box('LArPhaseBucket_shape',
                                        dx = self.Bucket_dx-self.Bucket_dd*2,
                                        dy = self.LAr_dy,
                                        dz = self.Bucket_dz-self.Bucket_dd*2)

        LArPhaseBucket_lv = geom.structure.Volume('volLArPhaseBucket',
                                        material=self.LArPhase_Material,
                                        shape=LArPhaseBucket_shape)

        # Place LAr Phase Bucket Volume inside Bucket volume
        pos = [Q('0cm'),-self.GAr_dy,Q('0cm')]

        LArPhaseBucket_pos = geom.structure.Position('LArPhaseBucket_pos',
                                                pos[0],pos[1],pos[2])

        LArPhaseBucket_pla = geom.structure.Placement('LArPhaseBucket_pla',
                                                volume=LArPhaseBucket_lv,
                                                pos=LArPhaseBucket_pos)

        main_lv.placements.append(LArPhaseBucket_pla.name)

        # Construct GAr Phase Bucket Volume
        GArPhaseBucket_shape = geom.shapes.Box('GArPhaseBucket_shape',
                                        dx = self.Bucket_dx-self.Bucket_dd*2,
                                        dy = self.GAr_dy,
                                        dz = self.Bucket_dz-self.Bucket_dd*2)

        GArPhaseBucket_lv = geom.structure.Volume('volGArPhaseBucket',
                                        material=self.GArPhase_Material,
                                        shape=GArPhaseBucket_shape)

        # Place GAr Phase Bucket Volume inside Bucket volume
        pos = [Q('0cm'),self.LAr_dy,Q('0cm')]

        GArPhaseBucket_pos = geom.structure.Position('GArPhaseBucket_pos',
                                                pos[0],pos[1],pos[2])

        GArPhaseBucket_pla = geom.structure.Placement('GArPhaseBucket_pla',
                                                volume=GArPhaseBucket_lv,
                                                pos=GArPhaseBucket_pos)

        main_lv.placements.append(GArPhaseBucket_pla.name)

        # Construct G10 Bottom Volume
        G10Bottom_shape = geom.shapes.Box('G10Bottom_shape',
                                        dx = self.G10Bottom_dx,
                                        dy = self.G10Bottom_dy,
                                        dz = self.G10Bottom_dz)

        G10Bottom_lv = geom.structure.Volume('volG10Bottom',
                                        material=self.Bucket_Material,
                                        shape=G10Bottom_shape)

        # Place G10 Bottom Volume inside Bucket volume
        pos = [Q('0cm'),-self.Bucket_dy+self.G10Bottom_dy,Q('0cm')]

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
        pos = [Q('0cm'),-self.Bucket_dy+self.LArVol1_dy+self.LArVol2_dy,Q('0cm')]

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
        pos = [Q('0cm'),-self.Bucket_dy+self.LArVol2_dy,Q('0cm')]

        LArVol2_pos = geom.structure.Position('LArVol2_pos',
                                                pos[0],pos[1],pos[2])

        LArVol2_pla = geom.structure.Placement('LArVol2_pla',
                                                volume=LArVol2_lv,
                                                pos=LArVol2_pos)

        main_lv.placements.append(LArVol2_pla.name)

