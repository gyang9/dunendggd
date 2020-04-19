""" OptSim.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class OptSimBuilder(gegede.builder.Builder):
    """ Class to build OptSim geometry.

    """

    def configure(self,Fieldcage_dimension,Bracket_dimension,Cathode_dx,**kwargs):

        # Read dimensions form config file
        self.Fieldcage_dx   = Fieldcage_dimension['dx']
        self.Fieldcage_dy   = Fieldcage_dimension['dy']
        self.Fieldcage_dz   = Fieldcage_dimension['dz']
        self.Fieldcage_dd   = Fieldcage_dimension['dd']

        self.Bracket_dx     = Bracket_dimension['dx']
        self.Bracket_dy     = Bracket_dimension['dy']
        self.Bracket_dz     = Bracket_dimension['dz']

        self.Cathode_dx     = Cathode_dx
        self.Kapton_dd      = Q('0.025mm')/2

        self.LAr_Material           = 'LAr'
        self.Bracket_Material       = 'G10'
        self.KaptonVolume_Material  = 'Kapton'

        # Material definitons
        self.Material               = 'G10'

        # Subbuilders
        self.TPC_builder         = self.get_builder('TPC')
        self.OpticalDet_builder  = self.TPC_builder.get_builder('OpticalDet')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Fieldcage_dx+self.Cathode_dx/2,
                                'dy':   self.Fieldcage_dy,
                                'dz':   self.Fieldcage_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('OptSimBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct Fieldcage
        Fieldcage_shape = geom.shapes.Box('Fieldcage_shape',
                                        dx = self.halfDimension['dx'],
                                        dy = self.halfDimension['dy'],
                                        dz = self.halfDimension['dz'])

        Fieldcage_lv = geom.structure.Volume('volFieldcage',
                                        material=self.Material,
                                        shape=Fieldcage_shape)

        # Place Fieldcage
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        Fieldcage_pos = geom.structure.Position('Fieldcage_pos',
                                                pos[0],pos[1],pos[2])

        Fieldcage_pla = geom.structure.Placement('Fieldcage_pla',
                                                volume=Fieldcage_lv,
                                                pos=Fieldcage_pos)

        main_lv.placements.append(Fieldcage_pla.name)

        # Construct Capton Volume
        KaptonVolume_shape = geom.shapes.Box('KaptonVolume_shape',
                                        dx = self.Fieldcage_dx-self.Cathode_dx/2+self.Kapton_dd,
                                        dy = self.Fieldcage_dy-self.Fieldcage_dd*2+self.Kapton_dd*2,
                                        dz = self.Fieldcage_dz-self.Fieldcage_dd*2+self.Kapton_dd*2)

        KaptonVolume_lv = geom.structure.Volume('volKaptonVolume',
                                        material=self.KaptonVolume_Material,
                                        shape=KaptonVolume_shape)

        # Place Capton Volume inside Fieldcage volume
        pos = [self.Kapton_dd,Q('0cm'),Q('0cm')]

        KaptonVolume_pos = geom.structure.Position('KaptonVolume_pos',
                                                pos[0],pos[1],pos[2])

        KaptonVolume_pla = geom.structure.Placement('KaptonVolume_pla',
                                                volume=KaptonVolume_lv,
                                                pos=KaptonVolume_pos)

        Fieldcage_lv.placements.append(KaptonVolume_pla.name)

        # Construct LAr Volume
        LAr_shape = geom.shapes.Box('LAr_shape',
                                        dx = self.Fieldcage_dx-self.Cathode_dx/2,
                                        dy = self.Fieldcage_dy-self.Fieldcage_dd*2,
                                        dz = self.Fieldcage_dz-self.Fieldcage_dd*2)

        LAr_lv = geom.structure.Volume('volLAr',
                                        material=self.LAr_Material,
                                        shape=LAr_shape)

        # Place LAr Volume inside Fieldcage volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        LAr_pos = geom.structure.Position('LAr_pos',
                                                pos[0],pos[1],pos[2])

        LAr_pla = geom.structure.Placement('LAr_pla',
                                                volume=LAr_lv,
                                                pos=LAr_pos)

        Fieldcage_lv.placements.append(LAr_pla.name)

        # Build TPC
        pos = [self.Fieldcage_dx-self.TPC_builder.halfDimension['dx']-self.Cathode_dx/2,Q('0cm'),Q('0cm')]

        TPC_lv = self.TPC_builder.get_volume()

        TPC_pos = geom.structure.Position(self.TPC_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        TPC_pla = geom.structure.Placement(self.TPC_builder.name+'_pla',
                                                volume=TPC_lv,
                                                pos=TPC_pos)

        LAr_lv.placements.append(TPC_pla.name)

        # Build OpticalDet L
        pos = [self.Fieldcage_dx-self.TPC_builder.halfDimension['dx']*2-self.Cathode_dx/2+self.OpticalDet_builder.halfDimension['dx'],Q('0cm'),-self.TPC_builder.halfDimension['dz']-self.OpticalDet_builder.halfDimension['dz']]

        OpticalDet_lv = self.OpticalDet_builder.get_volume()

        OpticalDet_pos = geom.structure.Position(self.OpticalDet_builder.name+'_pos_L',
                                                pos[0],pos[1],pos[2])

        OpticalDet_pla = geom.structure.Placement(self.OpticalDet_builder.name+'_pla_L',
                                                volume=OpticalDet_lv,
                                                pos=OpticalDet_pos)

        LAr_lv.placements.append(OpticalDet_pla.name)

        # Build OpticalDet R
        pos = [self.Fieldcage_dx-self.TPC_builder.halfDimension['dx']*2-self.Cathode_dx/2+self.OpticalDet_builder.halfDimension['dx'],Q('0cm'),+self.TPC_builder.halfDimension['dz']+self.OpticalDet_builder.halfDimension['dz']]

        OpticalDet_lv = self.OpticalDet_builder.get_volume()

        OpticalDet_pos = geom.structure.Position(self.OpticalDet_builder.name+'_pos_R',
                                                pos[0],pos[1],pos[2])

        rot = [Q('180.0deg'),Q('0.0deg'),Q('0.0deg')]

        OpticalDet_rot = geom.structure.Rotation(self.OpticalDet_builder.name+'_rot',
                                                rot[0],rot[1],rot[2])

        OpticalDet_pla = geom.structure.Placement(self.OpticalDet_builder.name+'_pla_R',
                                                volume=OpticalDet_lv,
                                                pos=OpticalDet_pos,
                                                rot=OpticalDet_rot)

        LAr_lv.placements.append(OpticalDet_pla.name)

        # Construct Bracket Volume
        Bracket_shape = geom.shapes.Box('Bracket_shape',
                                        dx = self.Bracket_dx,
                                        dy = self.Bracket_dy,
                                        dz = self.Bracket_dz)

        Bracket_lv = geom.structure.Volume('volBracket',
                                        material=self.Bracket_Material,
                                        shape=Bracket_shape)

        # Place Bracket Volume L inside Fieldcage volume
        pos = [self.Fieldcage_dx-self.Cathode_dx/2-self.Bracket_dx,Q('0cm'),-self.Fieldcage_dz+self.Fieldcage_dd*2+self.Bracket_dz]

        Bracket_pos = geom.structure.Position('Bracket_pos_L',
                                                pos[0],pos[1],pos[2])

        Bracket_pla = geom.structure.Placement('Bracket_pla_L',
                                                volume=Bracket_lv,
                                                pos=Bracket_pos)

        Fieldcage_lv.placements.append(Bracket_pla.name)

        # Place Bracket Volume R inside Fieldcage volume
        pos = [self.Fieldcage_dx-self.Cathode_dx/2-self.Bracket_dx,Q('0cm'),self.Fieldcage_dz-self.Fieldcage_dd*2-self.Bracket_dz]

        Bracket_pos = geom.structure.Position('Bracket_pos_R',
                                                pos[0],pos[1],pos[2])

        Bracket_pla = geom.structure.Placement('Bracket_pla_R',
                                                volume=Bracket_lv,
                                                pos=Bracket_pos)

        Fieldcage_lv.placements.append(Bracket_pla.name)

