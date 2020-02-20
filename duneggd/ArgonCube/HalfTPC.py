""" HalfTPC.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class HalfTPCBuilder(gegede.builder.Builder):
    """ Class to build HalfTPC geometry.

    """

    def configure(self,Gap_ASIC_G10,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.Gap_ASIC_G10 = Gap_ASIC_G10

        self.Material       = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        tpc_builder = self.get_builder('TPC')
        opticaldet_builder = self.get_builder('OpticalDet')

        self.halfDimension  = { 'dx':   opticaldet_builder.halfDimension['dx'] + self.Gap_ASIC_G10,
                                'dy':   tpc_builder.halfDimension['dy'],
                                'dz':   tpc_builder.halfDimension['dz']+2*opticaldet_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('HalfTPCBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build TPC
        pos = [self.Gap_ASIC_G10,Q('0cm'),Q('0cm')]

        tpc_lv = tpc_builder.get_volume()

        tpc_pos = geom.structure.Position(tpc_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        tpc_pla = geom.structure.Placement(tpc_builder.name+'_pla',
                                                volume=tpc_lv,
                                                pos=tpc_pos)

        main_lv.placements.append(tpc_pla.name)

        # Build OpticalDet L
        pos = [self.Gap_ASIC_G10,Q('0cm'),-tpc_builder.halfDimension['dz']-opticaldet_builder.halfDimension['dz']]

        opticaldet_lv = opticaldet_builder.get_volume()

        opticaldet_pos = geom.structure.Position(opticaldet_builder.name+'_pos_L',
                                                pos[0],pos[1],pos[2])

        opticaldet_pla = geom.structure.Placement(opticaldet_builder.name+'_pla_L',
                                                volume=opticaldet_lv,
                                                pos=opticaldet_pos)

        main_lv.placements.append(opticaldet_pla.name)

        # Build OpticalDet R
        pos = [self.Gap_ASIC_G10,Q('0cm'),+tpc_builder.halfDimension['dz']+opticaldet_builder.halfDimension['dz']]

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

        main_lv.placements.append(opticaldet_pla.name)


        # Place E-Field
        #main_lv.params.append(("EField",self.EField))
