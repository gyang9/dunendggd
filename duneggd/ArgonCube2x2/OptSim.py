""" OptSim.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class OptSimBuilder(gegede.builder.Builder):
    """ Class to build OptSim geometry.

    """

    def configure(self,Fieldcage_dimension,Bracket_dimension,Cathode_dx,Gap_ASIC_Backplate,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.Fieldcage_dx   = Fieldcage_dimension['dx']
        self.Fieldcage_dy   = Fieldcage_dimension['dy']
        self.Fieldcage_dz   = Fieldcage_dimension['dz']
        self.Fieldcage_dd   = Fieldcage_dimension['dd']

        self.Bracket_dx     = Bracket_dimension['dx']
        self.Bracket_dy     = Bracket_dimension['dy']
        self.Bracket_dz     = Bracket_dimension['dz']

        self.Cathode_dx     = Cathode_dx
        self.Kapton_dd      = Q('0.025mm')/2

        self.Gap_ASIC_Backplate     = Gap_ASIC_Backplate

        self.LAr_Material           = 'LAr'
        self.Bracket_Material       = 'G10'
        self.KaptonVolume_Material  = 'Kapton'

        self.Material               = 'G10'

    def construct(self,geom):
        """ Construct the geometry.

        """

        tpc_builder         = self.get_builder('TPC')
        opticaldet_builder  = tpc_builder.get_builder('OpticalDet')

        self.halfDimension  = { 'dx':   self.Fieldcage_dx+self.Cathode_dx/2,
                                'dy':   self.Fieldcage_dy,
                                'dz':   self.Fieldcage_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('OptSimBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Construct Fieldcage
        fieldcage_shape = geom.shapes.Box('Fieldcage',
                                        dx = self.halfDimension['dx'],
                                        dy = self.halfDimension['dy'],
                                        dz = self.halfDimension['dz'])

        fieldcage_lv = geom.structure.Volume('volFieldcage',
                                        material=self.Material,
                                        shape=fieldcage_shape)

        # Place Fieldcage
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        fieldcage_pos = geom.structure.Position('fieldcage_pos',
                                                pos[0],pos[1],pos[2])

        fieldcage_pla = geom.structure.Placement('fieldcage_pla',
                                                volume=fieldcage_lv,
                                                pos=fieldcage_pos)

        main_lv.placements.append(fieldcage_pla.name)

        # Construct Capton Volume
        kaptonVolume_shape = geom.shapes.Box('KaptonVolume',
                                        dx = self.Fieldcage_dx-self.Cathode_dx/2+self.Kapton_dd,
                                        dy = self.Fieldcage_dy-self.Fieldcage_dd*2+self.Kapton_dd*2,
                                        dz = self.Fieldcage_dz-self.Fieldcage_dd*2+self.Kapton_dd*2)

        kaptonVolume_lv = geom.structure.Volume('volKaptonVolume',
                                        material=self.KaptonVolume_Material,
                                        shape=kaptonVolume_shape)

        # Place Capton Volume inside Fieldcage volume
        pos = [self.Kapton_dd,Q('0cm'),Q('0cm')]

        kaptonVolume_pos = geom.structure.Position('kaptonVolume_pos',
                                                pos[0],pos[1],pos[2])

        kaptonVolume_pla = geom.structure.Placement('kaptonVolume_pla',
                                                volume=kaptonVolume_lv,
                                                pos=kaptonVolume_pos)

        fieldcage_lv.placements.append(kaptonVolume_pla.name)

        # Construct LAr Volume
        lar_shape = geom.shapes.Box('LAr',
                                        dx = self.Fieldcage_dx-self.Cathode_dx/2,
                                        dy = self.Fieldcage_dy-self.Fieldcage_dd*2,
                                        dz = self.Fieldcage_dz-self.Fieldcage_dd*2)

        lar_lv = geom.structure.Volume('volLAr',
                                        material=self.LAr_Material,
                                        shape=lar_shape)

        # Place LAr Volume inside Fieldcage volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        lar_pos = geom.structure.Position('lar_pos',
                                                pos[0],pos[1],pos[2])

        lar_pla = geom.structure.Placement('lar_pla',
                                                volume=lar_lv,
                                                pos=lar_pos)

        fieldcage_lv.placements.append(lar_pla.name)

        # Build TPC
        pos = [-self.Fieldcage_dx+tpc_builder.halfDimension['dx']+self.Cathode_dx/2+2*self.Gap_ASIC_Backplate,Q('0cm'),Q('0cm')]

        tpc_lv = tpc_builder.get_volume()

        tpc_pos = geom.structure.Position(tpc_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        tpc_pla = geom.structure.Placement(tpc_builder.name+'_pla',
                                                volume=tpc_lv,
                                                pos=tpc_pos)

        lar_lv.placements.append(tpc_pla.name)

        # Build OpticalDet L
        pos = [-self.Fieldcage_dx+opticaldet_builder.halfDimension['dx']+self.Cathode_dx/2+2*self.Gap_ASIC_Backplate,Q('0cm'),-tpc_builder.halfDimension['dz']-opticaldet_builder.halfDimension['dz']]

        opticaldet_lv = opticaldet_builder.get_volume()

        opticaldet_pos = geom.structure.Position(opticaldet_builder.name+'_pos_L',
                                                pos[0],pos[1],pos[2])

        opticaldet_pla = geom.structure.Placement(opticaldet_builder.name+'_pla_L',
                                                volume=opticaldet_lv,
                                                pos=opticaldet_pos)

        lar_lv.placements.append(opticaldet_pla.name)

        # Build OpticalDet R
        pos = [-self.Fieldcage_dx+opticaldet_builder.halfDimension['dx']+self.Cathode_dx/2+2*self.Gap_ASIC_Backplate,Q('0cm'),+tpc_builder.halfDimension['dz']+opticaldet_builder.halfDimension['dz']]

        opticaldet_lv = opticaldet_builder.get_volume()

        opticaldet_pos = geom.structure.Position(opticaldet_builder.name+'_pos_R',
                                                pos[0],pos[1],pos[2])

        rot_x = Q('180.0deg')

        opticaldet_rot = geom.structure.Rotation(opticaldet_builder.name+'_rot',
                                                x=rot_x)

        opticaldet_pla = geom.structure.Placement(opticaldet_builder.name+'_pla_R',
                                                volume=opticaldet_lv,
                                                pos=opticaldet_pos,
                                                rot=opticaldet_rot)

        lar_lv.placements.append(opticaldet_pla.name)

        # Construct Bracket Volume
        bracket_shape = geom.shapes.Box('Bracket',
                                        dx = self.Bracket_dx,
                                        dy = self.Bracket_dy,
                                        dz = self.Bracket_dz)

        bracket_lv = geom.structure.Volume('volBracket',
                                        material=self.Bracket_Material,
                                        shape=bracket_shape)

        # Place Bracket Volume L inside Fieldcage volume
        pos = [self.Fieldcage_dx-self.Cathode_dx/2-self.Bracket_dx,Q('0cm'),-self.Fieldcage_dz+self.Fieldcage_dd*2+self.Bracket_dz]

        bracket_pos = geom.structure.Position('bracket_pos_L',
                                                pos[0],pos[1],pos[2])

        bracket_pla = geom.structure.Placement('bracket_pla_L',
                                                volume=bracket_lv,
                                                pos=bracket_pos)

        fieldcage_lv.placements.append(bracket_pla.name)

        # Place Bracket Volume R inside Fieldcage volume
        pos = [self.Fieldcage_dx-self.Cathode_dx/2-self.Bracket_dx,Q('0cm'),self.Fieldcage_dz-self.Fieldcage_dd*2-self.Bracket_dz]

        bracket_pos = geom.structure.Position('bracket_pos_R',
                                                pos[0],pos[1],pos[2])

        bracket_pla = geom.structure.Placement('bracket_pla_R',
                                                volume=bracket_lv,
                                                pos=bracket_pos)

        fieldcage_lv.placements.append(bracket_pla.name)


        # Place E-Field
        #main_lv.params.append(("EField",self.EField))
