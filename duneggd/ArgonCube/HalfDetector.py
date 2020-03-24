""" HalfDetector.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class HalfDetectorBuilder(gegede.builder.Builder):
    """ Class to build HalfDetector geometry.

    """

    def configure(self,Fieldcage_dimension,Cathode_dx,Gap_ASIC_Backplate,**kwargs):

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

        self.Cathode_dx     = Cathode_dx

        self.Gap_ASIC_Backplate = Gap_ASIC_Backplate

        self.LArVolume_Material = 'LAr'
        self.Material           = 'G10'

    def construct(self,geom):
        """ Construct the geometry.

        """

        tpc_builder         = self.get_builder('TPC')
        opticaldet_builder  = tpc_builder.get_builder('OpticalDet')

        self.halfDimension  = { 'dx':   self.Fieldcage_dx,
                                'dy':   self.Fieldcage_dy,
                                'dz':   self.Fieldcage_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('HalfDetectorBuilder::construct()')
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

        # Construct LAr Volume
        larVolume_shape = geom.shapes.Box('LArVolume',
                                        dx = self.Fieldcage_dx-self.Cathode_dx/2,
                                        dy = self.Fieldcage_dy-self.Fieldcage_dd*2,
                                        dz = self.Fieldcage_dz-self.Fieldcage_dd*2)

        larVolume_lv = geom.structure.Volume('volLArVolume',
                                        material=self.LArVolume_Material,
                                        shape=larVolume_shape)

        # Place LAr Volume inside Fieldcage volume
        pos = [-self.Cathode_dx/2,Q('0cm'),Q('0cm')]

        larVolume_pos = geom.structure.Position('larVolume_pos',
                                                pos[0],pos[1],pos[2])

        larVolume_pla = geom.structure.Placement('larVolume_pla',
                                                volume=larVolume_lv,
                                                pos=larVolume_pos)

        fieldcage_lv.placements.append(larVolume_pla.name)

        # Build TPC
        pos = [-self.Fieldcage_dx+tpc_builder.halfDimension['dx']+self.Cathode_dx/2+2*self.Gap_ASIC_Backplate,Q('0cm'),Q('0cm')]

        tpc_lv = tpc_builder.get_volume()

        tpc_pos = geom.structure.Position(tpc_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        tpc_pla = geom.structure.Placement(tpc_builder.name+'_pla',
                                                volume=tpc_lv,
                                                pos=tpc_pos)

        larVolume_lv.placements.append(tpc_pla.name)

        # Build OpticalDet L
        pos = [-self.Fieldcage_dx+opticaldet_builder.halfDimension['dx']+self.Cathode_dx/2+2*self.Gap_ASIC_Backplate,Q('0cm'),-tpc_builder.halfDimension['dz']-opticaldet_builder.halfDimension['dz']]

        opticaldet_lv = opticaldet_builder.get_volume()

        opticaldet_pos = geom.structure.Position(opticaldet_builder.name+'_pos_L',
                                                pos[0],pos[1],pos[2])

        opticaldet_pla = geom.structure.Placement(opticaldet_builder.name+'_pla_L',
                                                volume=opticaldet_lv,
                                                pos=opticaldet_pos)

        larVolume_lv.placements.append(opticaldet_pla.name)

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

        larVolume_lv.placements.append(opticaldet_pla.name)


        # Place E-Field
        #main_lv.params.append(("EField",self.EField))
