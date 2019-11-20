""" PhotonSim.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class PhotonSimBuilder(gegede.builder.Builder):
    """ Class to build PhotonSim geometry.

    """

    def configure(self,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.Material       = 'G10'

    def construct(self,geom):
        """ Construct the geometry.

        """

        htpc_builder = self.get_builder('HalfTPC')

        self.halfDimension  = { 'dx':   htpc_builder.halfDimension['dx']+Q('1cm')/2,
                                'dy':   htpc_builder.halfDimension['dy']+Q('1cm')/2,
                                'dz':   htpc_builder.halfDimension['dz']+Q('1cm')/2}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('PhotonSimBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build HalfTPC
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        htpc_lv = htpc_builder.get_volume()

        htpc_pos = geom.structure.Position(htpc_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        htpc_pla = geom.structure.Placement(htpc_builder.name+'_pla',
                                                volume=htpc_lv,
                                                pos=htpc_pos)

        main_lv.placements.append(htpc_pla.name)

