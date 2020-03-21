""" TPCPlane.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class TPCPlaneBuilder(gegede.builder.Builder):
    """ Class to build TPCPlane geometry.

    """

    def configure(self,Gap_PixelTile,N_UnitsY,**kwargs):

        """ Set the configuration for the geometry.

            The keywords MaterialName and Density should only be used
            if Material is a dict-type rather than a string.

            Args:
                WLS_dimension: Outer dimensions of the WLS panel.
                    Dict. with keys 'dx', 'dy' and 'dz'
                kwargs: Additional keyword arguments. Allowed are:
        """

        self.Gap_PixelTile  = Gap_PixelTile
        self.N_UnitsY       = N_UnitsY

        self.Material       = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        pixelplane_builder  = self.get_builder('PixelPlane')

        self.halfDimension  = { 'dx':   pixelplane_builder.halfDimension['dx'],
                                'dy':   self.N_UnitsY*pixelplane_builder.halfDimension['dy']+(self.N_UnitsY-1)*self.Gap_PixelTile,
                                'dz':   2*pixelplane_builder.halfDimension['dz']+self.Gap_PixelTile}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('TPCPlaneBuilder::construct()')
        print('main_lv = '+main_lv.name)
        self.add_volume(main_lv)

        # Build TPC Array
        for i in range(self.N_UnitsY):
            pos = [Q('0cm'),(-self.N_UnitsY+1+2*i)*(pixelplane_builder.halfDimension['dy']+self.Gap_PixelTile),-pixelplane_builder.halfDimension['dz']-self.Gap_PixelTile]

            pixelplane_lv = pixelplane_builder.get_volume()

            pixelplane_pos = geom.structure.Position(pixelplane_builder.name+'_pos_'+str(i)+'R',
                                                pos[0],pos[1],pos[2])

            pixelplane_pla = geom.structure.Placement(pixelplane_builder.name+'_pla_'+str(i)+'R',
                                                    volume=pixelplane_lv,
                                                    pos=pixelplane_pos)

            main_lv.placements.append(pixelplane_pla.name)

        for i in range(self.N_UnitsY):
            pos = [Q('0cm'),(-self.N_UnitsY+1+2*i)*(pixelplane_builder.halfDimension['dy']+self.Gap_PixelTile),+pixelplane_builder.halfDimension['dz']+self.Gap_PixelTile]

            pixelplane_lv = pixelplane_builder.get_volume()

            pixelplane_pos = geom.structure.Position(pixelplane_builder.name+'_pos_'+str(i)+'L',
                                                pos[0],pos[1],pos[2])

            rot_x = Q('180.0deg')

            pixelplane_rot = geom.structure.Rotation(pixelplane_builder.name+'_rot_'+str(i)+'L',
                                                x=rot_x)

            pixelplane_pla = geom.structure.Placement(pixelplane_builder.name+'_pla_'+str(i)+'L',
                                                    volume=pixelplane_lv,
                                                    pos=pixelplane_pos,
                                                    rot=pixelplane_rot)

            main_lv.placements.append(pixelplane_pla.name)

        # Place E-Field
        #main_lv.params.append(("EField",self.EField))
