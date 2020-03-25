""" InnerDetector.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class InnerDetectorBuilder(gegede.builder.Builder):
    """ Class to build InnerDetector geometry.

    """

    def configure(self,**kwargs):

        # Material definitons
        self.Material           = 'G10'

    def construct(self,geom):
        """ Construct the geometry.

        """

        halfDetector_builder    = self.get_builder('HalfDetector')

        self.halfDimension  = { 'dx':   2*halfDetector_builder.halfDimension['dx'],
                                'dy':   halfDetector_builder.halfDimension['dy'],
                                'dz':   halfDetector_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('InnerDetectorBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build HalfDetector L
        pos = [-halfDetector_builder.halfDimension['dx'],Q('0cm'),Q('0cm')]

        halfDetector_lv = halfDetector_builder.get_volume()

        halfDetector_pos = geom.structure.Position(halfDetector_builder.name+'_pos_L',
                                                pos[0],pos[1],pos[2])

        halfDetector_pla = geom.structure.Placement(halfDetector_builder.name+'_pla_L',
                                                volume=halfDetector_lv,
                                                pos=halfDetector_pos)

        main_lv.placements.append(halfDetector_pla.name)

        # Build HalfDetector R
        pos = [halfDetector_builder.halfDimension['dx'],Q('0cm'),Q('0cm')]

        halfDetector_lv = halfDetector_builder.get_volume()

        halfDetector_pos = geom.structure.Position(halfDetector_builder.name+'_pos_R',
                                                pos[0],pos[1],pos[2])

        rot_y = Q('180.0deg')

        halfDetector_rot = geom.structure.Rotation(halfDetector_builder.name+'_rot',
                                                y=rot_y)

        halfDetector_pla = geom.structure.Placement(halfDetector_builder.name+'_pla_R',
                                                volume=halfDetector_lv,
                                                pos=halfDetector_pos,
                                                rot=halfDetector_rot)

        main_lv.placements.append(halfDetector_pla.name)

