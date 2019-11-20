""" HalfTPC.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class HalfTPCBuilder(gegede.builder.Builder):
    """ Class to build HalfTPC geometry.

    """

    def configure(self,N_UnitsY,EField,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.NUnits         = N_UnitsY
        self.EField         = EField

        self.Material       = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        lara_builder = self.get_builder('LArActive')

        self.halfDimension  = { 'dx':   lara_builder.halfDimension['dx'],
                                'dy':   self.NUnits*lara_builder.halfDimension['dy'],
                                'dz':   2*lara_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('HalfTPCBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build LArActive Array
        for i in range(self.NUnits):
            pos = [Q('0cm'),(-self.NUnits+1+2*i)*lara_builder.halfDimension['dy'],-lara_builder.halfDimension['dz']]

            lara_lv = lara_builder.get_volume()

            lara_pos = geom.structure.Position(lara_builder.name+'_pos_'+str(i)+'R',
                                                pos[0],pos[1],pos[2])

            lara_pla = geom.structure.Placement(lara_builder.name+'_pla_'+str(i)+'R',
                                                    volume=lara_lv,
                                                    pos=lara_pos)

            main_lv.placements.append(lara_pla.name)

        for i in range(self.NUnits):
            pos = [Q('0cm'),(-self.NUnits+1+2*i)*lara_builder.halfDimension['dy'],+lara_builder.halfDimension['dz']]

            lara_lv = lara_builder.get_volume()

            lara_pos = geom.structure.Position(lara_builder.name+'_pos_'+str(i)+'L',
                                                pos[0],pos[1],pos[2])

            rot_x = Q('180.0deg')

            lara_rot = geom.structure.Rotation(lara_builder.name+'_rot_'+str(i)+'L',
                                                x=rot_x)

            lara_pla = geom.structure.Placement(lara_builder.name+'_pla_'+str(i)+'L',
                                                    volume=lara_lv,
                                                    pos=lara_pos,
                                                    rot=lara_rot)

            main_lv.placements.append(lara_pla.name)

        # Place E-Field
        main_lv.params.append(("EField",self.EField))
